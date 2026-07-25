from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Risk = Literal["read", "write", "destructive"]
RunStatus = Literal["completed", "approval_required", "denied"]


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str
    tenant_id: str


@dataclass(frozen=True)
class ToolRequest:
    name: str
    risk: Risk
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceEvent:
    step: str
    detail: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    status: RunStatus
    answer: str
    citations: list[str]
    trace: list[TraceEvent]
    tool: str

