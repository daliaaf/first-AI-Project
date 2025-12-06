# agent_one_step.py
from pprint import pprint

from llm_client import agent_decide


def main():
    goal = "Create an outline for a 5-day AI learning plan."
    print("Sending goal to agent_decide():")
    print(goal)
    print("\n--- Agent decision (one step) ---\n")

    result = agent_decide(goal)

    pprint(result)  # pretty-print the dict so it's easier to read


if __name__ == "__main__":
    main()
