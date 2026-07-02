from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class StepStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class WorkflowStep:
    step_id: str
    name: str
    instruction: str
    required_output: str


@dataclass
class StepResult:
    step: WorkflowStep
    status: StepStatus
    output: str
    attempts: int = 1
    error: str | None = None


@dataclass(frozen=True)
class WorkflowPlan:
    task: str
    steps: list[WorkflowStep]


@dataclass(frozen=True)
class ValidationReport:
    approved: bool
    issues: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkflowRun:
    plan: WorkflowPlan
    results: list[StepResult]
    validation: ValidationReport
    event_log: list[str]
