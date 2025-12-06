# plan_one_step.py
from pprint import pprint

from llm_client import agent_plan


def main():
    goal = "Create a 5-day AI learning plan and save it to ai-plan.md"
    print("Planning for goal:")
    print(goal)
    print("\n--- Generated plan ---\n")

    plan = agent_plan(goal)
    pprint(plan)


if __name__ == "__main__":
    main()
