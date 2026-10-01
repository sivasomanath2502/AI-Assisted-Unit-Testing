import os
import time

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set in the .env file"
    )


client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


MODEL = "openrouter/free"

MAX_ATTEMPTS = 3
INITIAL_WAIT = 2


def ask_llm(prompt):
    last_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a code generation component. "
                            "Follow the user's instructions exactly. "
                            "Return only the requested output. "
                            "Do not provide explanations, reasoning, "
                            "Markdown fences, or commentary."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.1,
                max_tokens=4096,
            )

            content = response.choices[0].message.content

            if content and content.strip():
                return content.strip()

            last_error = "OpenRouter returned an empty response."

        except Exception as error:
            last_error = error

            error_text = str(error).lower()

            retryable = (
                "429" in error_text
                or "rate limit" in error_text
                or "temporarily" in error_text
                or "503" in error_text
                or "502" in error_text
                or "504" in error_text
                or "overloaded" in error_text
                or "upstream" in error_text
            )

            if not retryable:
                raise

        if attempt < MAX_ATTEMPTS:
            wait_time = INITIAL_WAIT * (2 ** (attempt - 1))

            print(
                f"LLM request failed "
                f"(attempt {attempt}/{MAX_ATTEMPTS}). "
                f"Retrying in {wait_time}s..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        f"LLM request failed after {MAX_ATTEMPTS} attempts: "
        f"{last_error}"
    )