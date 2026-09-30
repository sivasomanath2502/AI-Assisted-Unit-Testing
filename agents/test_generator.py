from llm_client import ask_llm


def generate_tests(code):

    prompt = f"""
You are a Python unit test generation agent.

Your task is to generate unit tests for the given Python function.

Testing objective:
Achieve branch coverage.

Requirements:
- Identify every decision point in the code.
- Generate tests that exercise both outcomes of every decision whenever possible.
- Include normal cases.
- Include boundary cases.
- Include edge cases.
- Write tests using pytest conventions.
- Do not import the target function.
- Assume the target function is already available in the same Python execution environment.
- The tests must call the actual function defined in the provided code.
- Do not modify the original function.
- Do not provide explanations.
- Do not use Markdown code fences.
- Return only raw Python test source code.
- The generated tests must be directly executable with pytest.

Code to test:

{code}
"""

    return ask_llm(prompt)


if __name__ == "__main__":

    code = """
def largest_element(lst):
    if not lst:
        return None

    max_val = lst[0]

    for num in lst:
        if num > max_val:
            max_val = num

    return max_val
"""

    tests = generate_tests(code)

    print(tests)