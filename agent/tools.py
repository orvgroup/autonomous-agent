
"""Safe tool registry for the ORVGROUP agent."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    requires_approval: bool = True


TOOL_REGISTRY: dict[str, Tool] = {}


def register_tool(tool: Tool) -> None:
    """Register an explicitly approved tool."""

    if not tool.name.strip():
        raise ValueError("Tool name cannot be empty.")

    if tool.name in TOOL_REGISTRY:
        raise ValueError(f"Tool already registered: {tool.name}")

    TOOL_REGISTRY[tool.name] = tool


def list_tools() -> list[dict[str, str]]:
    """Return descriptions of registered tools."""

    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in TOOL_REGISTRY.values()
    ]


def execute_tool(
    name: str,
    arguments: dict,
    approved: bool = False,
):
    """Execute a registered tool only when its safety rules allow it."""

    tool = TOOL_REGISTRY.get(name)

    if tool is None:
        raise ValueError(f"Unknown tool: {name}")

    if tool.requires_approval and not approved:
        raise PermissionError(
            f"Approval required before executing: {name}"
        )

    return tool.function(**arguments)
