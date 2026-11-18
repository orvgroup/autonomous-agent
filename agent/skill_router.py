
"""Route user tasks to relevant ORVGROUP skills."""

from agent.skill_loader import AVAILABLE_SKILLS, load_skill


SKILL_KEYWORDS = {
    "python-debugging": [
        "python", "bug", "debug", "error", "exception",
    ],
    "frontend-developer": [
        "frontend", "website", "html", "css", "react", "ui",
    ],
    "code-reviewer": [
        "review", "code quality", "security review", "audit",
    ],
    "api-developer": [
        "api", "endpoint", "rest", "backend service",
    ],
    "git-workflow": [
        "git", "github", "commit", "branch", "pull request",
    ],
    "database-engineer": [
        "database", "sql", "query", "schema", "postgres",
    ],
}


def route_task(task: str) -> list[str]:
    """Select skills based on task keywords."""

    if not task.strip():
        raise ValueError("Task cannot be empty.")

    text = task.lower()
    selected = []

    for skill_name in AVAILABLE_SKILLS:
        keywords = SKILL_KEYWORDS.get(skill_name, [])

        if any(keyword in text for keyword in keywords):
            selected.append(skill_name)

    return selected


def get_skills_for_task(task: str) -> dict[str, str]:
    """Load the selected skill instructions for a task."""

    skill_names = route_task(task)

    return {
        skill_name: load_skill(skill_name)
        for skill_name in skill_names
    }
