from __future__ import annotations

from .memory import TenantMemory
from .retrieval import TenantScopedRetriever
from .trust import TrustPolicy
from .types import Document, RunResult, ToolRequest, TraceEvent


WRITE_TERMS = {"deploy", "delete", "update", "change", "create"}


class AgenticRAGPlatform:
    """Provider-neutral agent loop with retrieval, policy, memory, and traces."""

    def __init__(self, documents: list[Document]):
        self.retriever = TenantScopedRetriever(documents)
        self.memory = TenantMemory()
        self.policy = TrustPolicy({"knowledge.search", "plan.create", "deployment.execute"})

    def _route(self, query: str) -> ToolRequest:
        terms = set(query.lower().split())
        if "deploy" in terms:
            return ToolRequest("deployment.execute", "write", {"query": query})
        if terms & WRITE_TERMS:
            return ToolRequest("plan.create", "write", {"query": query})
        return ToolRequest("knowledge.search", "read", {"query": query})

    def run(self, query: str, tenant_id: str, approved: bool = False) -> RunResult:
        trace = [TraceEvent("request.received", "accepted request", {"tenant_id": tenant_id})]
        request = self._route(query)
        trace.append(TraceEvent("router.selected", request.name, {"risk": request.risk}))
        decision = self.policy.evaluate(request, approved)
        trace.append(
            TraceEvent(
                "trust.evaluated",
                decision.reason,
                {"allowed": decision.allowed, "approval_required": decision.approval_required},
            )
        )
        if decision.approval_required:
            return RunResult(
                "approval_required",
                "This action changes state and requires explicit human approval.",
                [],
                trace,
                request.name,
            )
        if not decision.allowed:
            return RunResult("denied", decision.reason, [], trace, request.name)

        matches = self.retriever.search(query, tenant_id)
        trace.append(
            TraceEvent(
                "retrieval.completed",
                f"retrieved {len(matches)} tenant-scoped documents",
                {"document_ids": [document.id for document, _ in matches]},
            )
        )
        citations = [document.id for document, _ in matches]
        if matches:
            evidence = " ".join(
                f"{document.title}: {document.text} [{document.id}]" for document, _ in matches
            )
            answer = f"Grounded result: {evidence}"
        else:
            answer = "No grounded evidence was found for this tenant. No action was taken."
        self.memory.add(tenant_id, f"{request.name}:{','.join(citations) or 'none'}")
        trace.append(TraceEvent("run.completed", "result returned with explicit citations"))
        return RunResult("completed", answer, citations, trace, request.name)

