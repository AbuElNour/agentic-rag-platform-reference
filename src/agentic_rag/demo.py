from __future__ import annotations

import json
from dataclasses import asdict

from .orchestrator import AgenticRAGPlatform
from .types import Document


def main() -> None:
    platform = AgenticRAGPlatform(
        [
            Document("policy-001", "Deployment policy", "Production changes require approval.", "demo"),
            Document("rag-001", "Retrieval design", "Hybrid retrieval combines keyword and vector search.", "demo"),
            Document("other-001", "Private tenant note", "This must never cross tenant boundaries.", "other"),
        ]
    )
    for query in ("How does retrieval work?", "Deploy this change"):
        result = platform.run(query, tenant_id="demo")
        print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()

