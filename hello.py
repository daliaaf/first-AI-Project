
import os
import openai
import tiktoken

from dotenv import load_dotenv, find_dotenv

load_dotenv()  # reads .env into os.environ
openai.api_key = os.getenv("OPENAI_API_KEY")



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    # ← note: `chat.completions.create`, not `ChatCompletion.create`
    response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
    )
    return response.choices[0].message.content


def get_completion_from_messages(messages,
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=500):
    response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
            max_tokens=max_tokens, # the maximum number of tokens the model can ouptut
    )
    # return response.choices[0].message["content"]
    return response.choices[0].message.content

# print(get_completion("What is the capital of France?"))

messages =  [
    {'role':'system',
     'content':"""You are an assistant who\
 responds in the style of Dr Seuss."""},
    {'role':'user',
     'content':"""write me a very short poem\
 about a happy carrot"""},
]
response = get_completion_from_messages(messages, temperature=1)
print(response)


# length
messages =  [
    {'role':'system',
     'content':'All your responses must be \
one sentence long.'},
    {'role':'user',
     'content':'write me a story about a happy carrot'},
]
response = get_completion_from_messages(messages, temperature =1)
print(response)

# combined
messages =  [
    {'role':'system',
     'content':"""You are an assistant who \
responds in the style of Dr Seuss. \
All your responses must be one sentence long."""},
    {'role':'user',
     'content':"""write me a story about a happy carrot"""},
]
response = get_completion_from_messages(messages,
                                        temperature =1)
print(response)
