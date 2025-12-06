# agent_runner.py
import sys
from pprint import pprint
from typing import Optional

from llm_client import agent_decide
from tools import (
    write_file,
    read_file,
    list_files,
    append_file,
    calculate,
    search_in_file,
    remember,
    recall,
)


# Map action names (strings) to actual Python functions
# Python needs to run the actual function write_file.
TOOLS = {
    "write_file": write_file,
    "read_file": read_file,
    "list_files": list_files,
    "append_file": append_file,
    "calculate": calculate,
    "search_in_file": search_in_file,
    "remember": remember,
    "recall": recall,
}


def run_agent(goal: str, max_steps: int = 15) -> None:
    """
    Run the agent loop for a given goal.
    - goal: what we want to achieve (natural language).
    - max_steps: safety limit to avoid infinite loops.
    """
    observation: Optional[str] = None

    print(f"Agent starting with goal:\n  {goal}")
    print("=" * 50)

    for step in range(1, max_steps + 1):
        print(f"\n--- STEP {step} ---")

        # Ask the model what to do next
        decision = agent_decide(goal, observation=observation)

        # Show the raw decision (for debugging/learning)
        print("Decision JSON:")
        pprint(decision)

        thought = decision.get("thought")
        action = decision.get("action")
        args = decision.get("args") or {}
        done = decision.get("done")
        final_answer = decision.get("final_answer")

        if thought:
            print("\nThought:", thought)

        # If the model says we're done, show final answer and stop
        if done:
            print("\n✅ Agent finished.")
            if final_answer:
                print("\nFinal answer:\n")
                print(final_answer)
            else:
                print("(No final_answer provided.)")
            return

        # If not done, there should be an action
        if not action:
            print("\n⚠️ No action provided, stopping.")
            return

        tool_fn = TOOLS.get(action)
        if not tool_fn:
            print(f"\n⚠️ Unknown action '{action}', stopping.")
            return

        print(f"\n▶ Running tool: {action} with args: {args}")

        try:
            # Call the selected tool with the provided args
            result = tool_fn(**args)
        except TypeError as e:
            print(f"\n⚠️ Error when calling tool '{action}': {e}")
            return

        print("\nTool result:\n")
        print(result)

        # The tool result becomes the next observation for the model
        observation = result

    print(f"\n⏹ Reached max steps ({max_steps}) without finishing.")


def main():
    # Allow passing the goal via command line:
    #   python agent_runner.py "Create a 5-day AI plan and save it to ai-plan.md"
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
    else:
        # Or ask interactively if no arguments are given
        print("Enter the agent's goal:")
        goal = input("> ")

    run_agent(goal)


if __name__ == "__main__":
    main()
