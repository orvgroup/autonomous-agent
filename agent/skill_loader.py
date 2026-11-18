
"""Load reusable skills from the ORVGROUP Agent Skills Hub."""

from pathlib import Path
from urllib.request import urlopen


SKILLS_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "orvgroup/agent-skills-hub/main/skills"
)

AVAILABLE_SKILLS = [
    "python-debugging",
    "frontend-developer",
    "code-reviewer",
    "api-developer",
    "git-workflow",
    "database-engineer",
]


def load_skill(skill_name: str) -> str:
    """Download and return a skill instruction file."""

    if skill_name not in AVAILABLE_SKILLS:
        raise ValueError(f"Unknown skill: {skill_name}")

    url = f"{SKILLS_BASE_URL}/{skill_name}/SKILL.md"

    with urlopen(url, timeout=15) as response:
        content = response.read().decode("utf-8")

    if not content.strip():
        raise ValueError(f"Skill is empty: {skill_name}")

    return content


def list_skills() -> list[str]:
    """Return available skill names."""
    return AVAILABLE_SKILLS.copy()
