
"""Command-line interface for the ORVGROUP agent."""

import argparse
import json

from agent.core import run_agent


def main() -> None:
    """Run the agent from the command line."""

    parser = argparse.ArgumentParser(
        description="ORVGROUP Autonomous AI Agent"
    )

    parser.add_argument(
        "goal",
        help="The task you want the agent to handle.",
    )

    args = parser.parse_args()

    try:
        result = run_agent(args.goal)
        print(json.dumps(result, indent=2))
    except Exception as error:
        print(f"Agent error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
