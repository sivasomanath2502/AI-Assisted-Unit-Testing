from pathlib import Path

from llm_client import ask_llm
from utils.artifact_validator import validate_tests


PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "test_generator_prompt.txt"

RETRY_PROMPT = """
The previous response was not valid pytest source code.

Generate the tests again for the Python function below.

STRICT OUTPUT RULE:
Return ONLY executable Python source code.
The response MUST:
- import pytest if pytest features are needed
- import the target function from solution
- contain at least one function whose name starts with test_
- contain no reasoning, analysis, safety messages, Markdown fences,
  explanations, or commentary
- contain nothing before or after the Python code

Testing objective:
Achieve branch coverage by exercising both outcomes of decisions
whenever possible, including normal, boundary, and edge cases.

Code to test:
{code}
"""


def generate_tests(code):
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    prompt = prompt_template.format(code=code)

    last_error = None

    for attempt in range(3):
        current_prompt = prompt if attempt == 0 else RETRY_PROMPT.format(
            code=code
        )

        raw_tests = ask_llm(current_prompt)

        is_valid, cleaned_tests, error = validate_tests(raw_tests)

        if is_valid:
            return cleaned_tests

        last_error = error

    raise ValueError(
        f"TEST_GENERATION_FAILED after 3 attempts: {last_error}"
    )
