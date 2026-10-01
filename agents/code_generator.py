from pathlib import Path

from llm_client import ask_llm
from utils.artifact_validator import validate_code


PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "code_generator_prompt.txt"

RETRY_PROMPT = """
The previous response was not valid Python source code.

Generate the solution again.

STRICT OUTPUT RULE:
Return ONLY executable Python source code.
Do not include reasoning, analysis, safety messages, Markdown fences,
explanations, or any text before or after the Python code.
The response must contain at least one Python function.

Problem:
{problem}
"""


def generate_code(problem):
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    prompt = prompt_template.format(problem=problem)

    last_error = None

    for attempt in range(3):
        current_prompt = prompt if attempt == 0 else RETRY_PROMPT.format(
            problem=problem
        )

        raw_code = ask_llm(current_prompt)

        is_valid, cleaned_code, error = validate_code(raw_code)

        if is_valid:
            return cleaned_code

        last_error = error

    raise ValueError(
        f"CODE_GENERATION_FAILED after 3 attempts: {last_error}"
    )
