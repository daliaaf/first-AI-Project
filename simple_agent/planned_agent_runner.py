# planned_agent_runner.py
from pprint import pprint

from llm_client import agent_plan
from agent_runner import run_agent


def run_planned_agent(goal: str, max_steps_per_subgoal: int = 5) -> None:
    """
    1) Ask the LLM to create a plan for the goal.
    2) Execute each step in order using run_agent.
    """
    print("✨ Planning phase")
    print("================")
    print("Main goal:")
    print(f"  {goal}\n")

    plan = agent_plan(goal)

    steps = plan.get("steps", [])
    if not steps:
        print("⚠️ No steps returned from planner, aborting.")
        pprint(plan)
        return

    print("Generated plan:")
    for step in steps:
        sid = step.get("id")
        desc = step.get("description")
        print(f"  Step {sid}: {desc}")

    print("\n🛠 Execution phase")
    print("=================")

    for step in steps:
        sid = step.get("id")
        desc = step.get("description")

        print(f"\n==============================")
        print(f"🚀 Executing step {sid}: {desc}")
        print(f"==============================\n")

        # We use the step description as a sub-goal.
        # Optionally include the main goal for extra context:
        subgoal = f"(Main goal: {goal})\nSub-goal: {desc}"

        # Call the existing agent runner for each step
        run_agent(subgoal, max_steps=max_steps_per_subgoal)


def main():
    print("Enter the MAIN goal for the planned agent:")
    goal = input("> ").strip()
    if not goal:
        print("No goal entered, exiting.")
        return

    run_planned_agent(goal)


if __name__ == "__main__":
    main()
