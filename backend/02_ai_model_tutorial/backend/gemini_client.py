from config import Config
from google import genai

client = genai.Client(api_key=Config.gemini_api_key)


def get_answer_from_gemini(prompt: str):
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return response.text
