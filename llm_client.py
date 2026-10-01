import requests


OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL = "qwen2.5-coder:7b"


def ask_llm(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a code generation component. "
                        "Return only the requested Python source code. "
                        "Do not provide explanations, reasoning, "
                        "Markdown fences, or commentary."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    content = data["message"]["content"]

    if not content:
        raise RuntimeError("Ollama returned an empty response")

    return content