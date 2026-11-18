
"""Basic task planner for the ORVGROUP agent."""

from agent.models import TaskPlan, TaskStep


def create_plan(goal: str) -> TaskPlan:
    """Create a simple initial plan for a user goal."""

    cleaned_goal = goal.strip()

    if not cleaned_goal:
        raise ValueError("Goal cannot be empty.")

    steps = [
        TaskStep(
            step_id=1,
            description=f"Understand the requirements: {cleaned_goal}",
        ),
        TaskStep(
            step_id=2,
            description="Identify the skills and tools required.",
        ),
        TaskStep(
            step_id=3,
            description="Prepare an execution approach.",
        ),
        TaskStep(
            step_id=4,
            description="Execute approved actions.",
        ),
        TaskStep(
            step_id=5,
            description="Verify the results and report completion.",
        ),
    ]

    return TaskPlan(goal=cleaned_goal, steps=steps)
