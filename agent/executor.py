
"""Execution engine for the ORVGROUP autonomous agent."""

from agent.models import TaskPlan, TaskStatus
from agent.planner import create_plan


def execute_plan(plan: TaskPlan) -> TaskPlan:
    """Process a plan through its steps."""

    if not plan.steps:
        plan.status = TaskStatus.FAILED
        return plan

    plan.status = TaskStatus.IN_PROGRESS

    for step in plan.steps:
        step.status = TaskStatus.IN_PROGRESS

        # Execution actions will be connected in later stages.
        step.result = "Step prepared; action execution not yet connected."
        step.status = TaskStatus.COMPLETED

    plan.status = (
        TaskStatus.COMPLETED
        if plan.is_complete()
        else TaskStatus.FAILED
    )

    return plan


def run_task(goal: str) -> TaskPlan:
    """Create and process a task plan."""

    plan = create_plan(goal)
    return execute_plan(plan)
