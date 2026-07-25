from __future__ import annotations

from dataclasses import dataclass

from .types import ToolRequest


@dataclass(frozen=True)
class TrustDecision:
    allowed: bool
    approval_required: bool
    reason: str


class TrustPolicy:
    """Explicit policy for tool scopes and human approval."""

    def __init__(self, allowed_tools: set[str]):
        self._allowed_tools = frozenset(allowed_tools)

    def evaluate(self, request: ToolRequest, approved: bool) -> TrustDecision:
        if request.name not in self._allowed_tools:
            return TrustDecision(False, False, "tool is outside the configured allowlist")
        if request.risk in {"write", "destructive"} and not approved:
            return TrustDecision(False, True, "human approval is required for state-changing tools")
        return TrustDecision(True, False, "policy checks passed")

