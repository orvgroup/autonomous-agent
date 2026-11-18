
"""Data models for agent tasks and execution plans."""

from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_APPROVAL = "needs_approval"


@dataclass
class TaskStep:
    step_id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    result: str = ""


@dataclass
class TaskPlan:
    goal: str
    steps: list[TaskStep] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING

    def is_complete(self) -> bool:
        """Return True when every planned step is complete."""
        return bool(self.steps) and all(
            step.status == TaskStatus.COMPLETED
            for step in self.steps
        )
