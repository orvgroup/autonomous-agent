
"""Main entry point for the ORVGROUP Autonomous AI Agent."""

from agent.executor import run_task
from agent.llm import generate_response
from agent.skill_router import get_skills_for_task


def run_agent(goal: str) -> dict:
    """Run the agent workflow for a user goal."""

    if not goal.strip():
        raise ValueError("Goal cannot be empty.")

    skills = get_skills_for_task(goal)

    skill_context = "\n\n".join(
        f"## Skill: {name}\n{content}"
        for name, content in skills.items()
    )

    prompt = (
        "You are the ORVGROUP Autonomous AI Agent.\n"
        "Analyze the user's goal using the available skill instructions.\n"
        "Do not claim to have performed actions that you have not performed.\n\n"
        f"{skill_context}\n\n"
        f"User goal: {goal}"
    )

    ai_response = generate_response(prompt)
    execution_plan = run_task(goal)

    return {
        "goal": goal,
        "selected_skills": list(skills.keys()),
        "ai_response": ai_response,
        "execution_status": execution_plan.status.value,
        "execution_plan": [
            {
                "step": step.description,
                "status": step.status.value,
                "result": step.result,
            }
            for step in execution_plan.steps
        ],
    }
