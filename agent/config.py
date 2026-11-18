
"""Configuration for the ORVGROUP autonomous agent."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    model: str = "gpt-4.1-mini"
    max_steps: int = 10
    require_approval: bool = True
    skills_repository: str = (
        "https://github.com/orvgroup/agent-skills-hub"
    )


def load_config() -> AgentConfig:
    """Load agent configuration from environment variables."""
    return AgentConfig(
        model=os.getenv("ORVGROUP_MODEL", "gpt-4.1-mini"),
        max_steps=int(os.getenv("ORVGROUP_MAX_STEPS", "10")),
        require_approval=os.getenv(
            "ORVGROUP_REQUIRE_APPROVAL", "true"
        ).lower() == "true",
    )
