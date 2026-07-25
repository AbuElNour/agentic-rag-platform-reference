from __future__ import annotations

from collections import defaultdict


class TenantMemory:
    def __init__(self) -> None:
        self._items: dict[str, list[str]] = defaultdict(list)

    def add(self, tenant_id: str, item: str) -> None:
        self._items[tenant_id].append(item)

    def recent(self, tenant_id: str, limit: int = 5) -> tuple[str, ...]:
        return tuple(self._items[tenant_id][-limit:])

