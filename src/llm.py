from openai import OpenAI
#from src.prompt import health_prompts
from src.prompt import chinese_language_prompts


client = OpenAI()

messages = [
    {"role": "system", "content": chinese_language_prompts}
]


default_openai_model= "gpt-4"
default_temperature = 0.1

def ask_openai(messages, model=default_openai_model,temperature=default_temperature):
    print(messages)
    response = client.chat.completions.create(
        model= model,
        messages=  messages,
        temperature= temperature 
    )

    return response.choices[0].message.content
