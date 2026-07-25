from __future__ import annotations

import math
import re
from collections import Counter

from .types import Document


TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


class TenantScopedRetriever:
    """Small deterministic retriever that demonstrates tenant isolation."""

    def __init__(self, documents: list[Document]):
        self._documents = tuple(documents)

    def search(self, query: str, tenant_id: str, top_k: int = 3) -> list[tuple[Document, float]]:
        query_terms = Counter(tokenize(query))
        if not query_terms:
            return []

        candidates = [document for document in self._documents if document.tenant_id == tenant_id]
        document_frequency = Counter(
            term for document in candidates for term in set(tokenize(document.title + " " + document.text))
        )
        scored: list[tuple[Document, float]] = []
        for document in candidates:
            terms = Counter(tokenize(document.title + " " + document.text))
            score = 0.0
            for term, count in query_terms.items():
                if term not in terms:
                    continue
                inverse_frequency = math.log((len(candidates) + 1) / (document_frequency[term] + 1)) + 1
                score += min(terms[term], count) * inverse_frequency
            if score:
                scored.append((document, round(score, 4)))
        return sorted(scored, key=lambda item: (-item[1], item[0].id))[:top_k]

