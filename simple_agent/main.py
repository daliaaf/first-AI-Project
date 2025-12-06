# main.py
from llm_client import ask_llm


def main():
    print("Simple LLM test. Type a question and press Enter.")
    user_input = input("You: ")

    reply = ask_llm(user_input)
    print("\nAssistant:", reply)


if __name__ == "__main__":
    main()
