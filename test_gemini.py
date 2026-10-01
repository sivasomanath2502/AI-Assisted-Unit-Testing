from llm_client import ask_llm


prompt = """
Write a Python function named square_perimeter
that takes one argument called side.

Return only the Python code.
Do not use Markdown.
Do not explain anything.
"""


result = ask_llm(prompt)

print(result)