# llm_client.py
import os
import json
from typing import Optional

from openai import OpenAI

# Load the API key from the environment and create a client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm(prompt: str) -> str:
    """
    Send a simple prompt to the LLM and return the text response.
    This is just to confirm everything works.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
    )

    return response.choices[0].message.content


# decision brain
def agent_decide(goal: str, observation: Optional[str] = None) -> dict:
    """
    Ask the LLM to act like an agent and return a JSON object with:
    - thought: string
    - action: string or null
    - args: object (dict) or null
    - done: boolean
    - final_answer: string or null
    """

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    system_prompt = """
You are an AI agent controller.

Your job is to think step-by-step and decide what to do next
to achieve the user's GOAL.

Available tools (actions) you can choose:
- "write_file": args: { "path": string, "content": string }
- "read_file": args: { "path": string }
- "list_files": args: { } (no arguments)
- "append_file": args: { "path": string, "content": string }
- "calculate": args: { "expression": string }
- "search_in_file": args: { "path": string, "query": string }
- "remember": args: { "content": string }   // store long-term notes in memory.txt
- "recall": args: { }                       // read back all stored memory

You MUST ALWAYS respond with a JSON object with the following keys:

{
  "thought": "string - your internal reasoning in simple language",
  "action": "string or null - the name of the tool you want to use, e.g. 'write_file', 'read_file', 'list_files', or null if you are finished",
  "args": { } or null - a JSON object with arguments for the action (for example: { "path": "plan.md", "content": "..." }),
  "done": true or false,
  "final_answer": "string or null - if done is true, this is the final answer for the user"
}

Rules:
- If you still need to take an action, set "done": false and "final_answer": null.
- If you are finished, set "done": true and fill "final_answer" with a helpful message.
- Never output anything that is not valid JSON.
- Do not include comments or markdown in the JSON.
    """.strip()


    user_content = f"GOAL: {goal}"
    if observation:
        user_content += f"\nLATEST_OBSERVATION: {observation}"

    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
    )

    raw_json = response.choices[0].message.content
    # raw_json is a string like '{"thought": "...", "action": "...", ...}'
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Model returned invalid JSON: {raw_json}") from e

    return data

def agent_plan(goal: str) -> dict:
    """
    Ask the LLM to create a step-by-step plan for the given goal.

    Returns a dict like:
    {
      "steps": [
        {"id": 1, "description": "..."},
        {"id": 2, "description": "..."},
        ...
      ]
    }
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    system_prompt = """
You are a planning assistant for an AI agent.

Your job is to break the user's GOAL into a small number of clear,
ordered steps that another agent can execute.

You MUST respond with a JSON object with this shape:

{
  "steps": [
    {
      "id": 1,
      "description": "First do this..."
    },
    {
      "id": 2,
      "description": "Then do that..."
    }
  ]
}

Rules:
- Use a small number of steps (3–7) unless the goal is huge.
- Make each description specific and actionable.
- Do NOT include any other keys besides "steps", "id", and "description".
- Do NOT include comments or markdown, only valid JSON.
""".strip()

    user_content = f"GOAL: {goal}"

    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
    )

    raw_json = response.choices[0].message.content

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Model returned invalid JSON in agent_plan: {raw_json}") from e

    return data
