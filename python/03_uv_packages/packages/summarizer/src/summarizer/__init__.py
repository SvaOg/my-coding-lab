from google import genai
from google.genai import types


def summarize_text(text: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction="You are a text summary writer"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Summarize the following text:\n\n{text}",
        config=config,
    )

    return response.text
