"""Tests for the ORVGROUP tool registry."""

import pytest

from agent.tools import (
    TOOL_REGISTRY,
    Tool,
    register_tool,
    list_tools,
    execute_tool,
)


@pytest.fixture(autouse=True)
def clear_registry():
    TOOL_REGISTRY.clear()
    yield
    TOOL_REGISTRY.clear()


def test_register_tool():
    tool = Tool("greet", "Greet a user", lambda: "Hello")

    register_tool(tool)

    assert "greet" in TOOL_REGISTRY


def test_rejects_empty_tool_name():
    tool = Tool("", "Invalid tool", lambda: None)

    with pytest.raises(ValueError):
        register_tool(tool)


def test_rejects_duplicate_tool():
    tool = Tool("greet", "Greet a user", lambda: "Hello")

    register_tool(tool)

    with pytest.raises(ValueError):
        register_tool(tool)


def test_lists_registered_tools():
    tool = Tool("greet", "Greet a user", lambda: "Hello")

    register_tool(tool)

    tools = list_tools()

    assert tools[0]["name"] == "greet"


def test_requires_approval():
    tool = Tool("delete_file", "Delete a file", lambda: "Deleted")

    register_tool(tool)

    with pytest.raises(PermissionError):
        execute_tool("delete_file", {})


def test_executes_approved_tool():
    tool = Tool(
        "greet",
        "Greet a user",
        lambda name: f"Hello {name}",
    )

    register_tool(tool)

    result = execute_tool(
        "greet",
        {"name": "Agent"},
        approved=True,
    )

    assert result == "Hello Agent"


def test_rejects_unknown_tool():
    with pytest.raises(ValueError):
        execute_tool("unknown", {})
