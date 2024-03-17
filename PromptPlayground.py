from openai import AsyncOpenAI

from chainlit.playground.providers import ChatOpenAI
import chainlit as cl
import os
import dotenv

dotenv.load_dotenv() 

from groq import Groq

clientG = Groq(
        api_key = os.getenv('GROQ_API_KEY')
)


client = AsyncOpenAI()

template = "Hello, {name}!"
variables = {"name": "Ben"}

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    # ... more settings
}


@cl.step(type="llm")
async def call_llm():
    generation = cl.ChatGeneration(
        provider=ChatOpenAI.id,
        variables=variables,
        settings=settings,
        messages=[
            {
                "content": template.format(**variables),
                "role":"user"
            },
            {
                "content": """Please always answer in Traditional Chinese. Start by telling a joke about Taiwan in Traditional Chinese""",
                "role":"system"
            },
        ],
    )

    # Make the call to OpenAI
    response = clientG.chat.completions.create(
        messages=generation.messages,
        model="mixtral-8x7b-32768",
        #**settings
    )

    generation.message_completion = {
        "content": response.choices[0].message.content,
        "role": "assistant"
    }

    # Add the generation to the current step
    cl.context.current_step.generation = generation

    return generation.message_completion["content"]


@cl.on_chat_start
async def start():
    await call_llm()
