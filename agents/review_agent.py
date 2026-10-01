from pathlib import Path

from llm_client import ask_llm


PROMPT_FILE = (
    Path(__file__).parent.parent
    / "prompts"
    / "review_agent_prompt.txt"
)


def _parse_review_response(response):
    """
    Extract APPROVE or REJECT from the Review Agent response.
    """

    for line in response.splitlines():

        line = line.strip().upper()

        if line.startswith("VERDICT:"):

            verdict = (
                line
                .split(":", 1)[1]
                .strip()
            )

            if verdict in {
                "APPROVE",
                "REJECT",
            }:
                return verdict

    return None


def review_tests(
    problem,
    code,
    function_name,
    reference_tests,
    tests,
    max_attempts=2,
):
    prompt_template = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

    reference_examples = "\n".join(
        reference_tests
    )

    base_prompt = prompt_template.format(
        problem=problem,
        code=code,
        function_name=function_name,
        reference_tests=reference_examples,
        tests=tests,
    )

    prompt = base_prompt

    last_response = None

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        response = ask_llm(prompt)

        last_response = response

        verdict = _parse_review_response(
            response
        )

        if verdict is not None:

            return {
                "verdict": verdict,
                "response": response.strip(),
                "approved": verdict == "APPROVE",
                "attempts": attempt,
            }

        if attempt < max_attempts:

            prompt = (
                base_prompt
                + "\n\n"
                "IMPORTANT: Your previous response "
                "did not follow the required format.\n"
                "\n"
                "You MUST return exactly one of these "
                "verdict lines:\n"
                "\n"
                "VERDICT: APPROVE\n"
                "\n"
                "or:\n"
                "\n"
                "VERDICT: REJECT\n"
                "\n"
                "Then provide:\n"
                "REASONS:\n"
                "- reason 1\n"
                "- reason 2\n"
                "\n"
                "Do not output safety classifications, "
                "metadata, commentary, or any other format."
            )

    raise RuntimeError(
        "REVIEW_FAILED: Review Agent did not return "
        "a valid APPROVE or REJECT verdict after "
        f"{max_attempts} attempts.\n\n"
        "Last Review Agent response:\n"
        f"{last_response}"
    )