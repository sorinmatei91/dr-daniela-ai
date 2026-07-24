import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60
)


def generate_ai_response(system_prompt, conversation):
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=conversation,
        max_output_tokens=250
    )

    return response.output_text