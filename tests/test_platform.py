from __future__ import annotations

import unittest

from agentic_rag import AgenticRAGPlatform, Document


class PlatformTests(unittest.TestCase):
    def setUp(self) -> None:
        self.platform = AgenticRAGPlatform(
            [
                Document("a-policy", "Approval policy", "Deployments require human approval.", "tenant-a"),
                Document("a-rag", "RAG", "Retrieval returns grounded citations.", "tenant-a"),
                Document("b-secret", "Internal plan", "Tenant B confidential roadmap.", "tenant-b"),
            ]
        )

    def test_retrieval_is_tenant_scoped(self) -> None:
        result = self.platform.run("confidential roadmap", "tenant-a")
        self.assertNotIn("b-secret", result.citations)
        self.assertNotIn("Tenant B", result.answer)

    def test_read_tool_completes(self) -> None:
        result = self.platform.run("How does retrieval return citations?", "tenant-a")
        self.assertEqual(result.status, "completed")
        self.assertIn("a-rag", result.citations)

    def test_write_requires_approval(self) -> None:
        result = self.platform.run("Deploy the latest plan", "tenant-a")
        self.assertEqual(result.status, "approval_required")
        self.assertEqual(result.citations, [])

    def test_approved_write_is_grounded(self) -> None:
        result = self.platform.run("Deploy according to the approval policy", "tenant-a", approved=True)
        self.assertEqual(result.status, "completed")
        self.assertIn("a-policy", result.citations)

    def test_trace_contains_policy_and_retrieval(self) -> None:
        result = self.platform.run("retrieval", "tenant-a")
        steps = [event.step for event in result.trace]
        self.assertIn("trust.evaluated", steps)
        self.assertIn("retrieval.completed", steps)


if __name__ == "__main__":
    unittest.main()

