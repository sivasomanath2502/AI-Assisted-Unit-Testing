import ast
import re


def _remove_code_fences(text):
    text = text.strip()

    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()

        if len(lines) >= 2:
            lines = lines[1:-1]
            text = "\n".join(lines).strip()

    return text


def _contains_reasoning(text):
    lowered = text.lower()

    forbidden_markers = [
        "<think>",
        "</think>",
        "user safety:",
        "here is the code:",
        "here's the code:",
        "here are the tests:",
        "sure, here",
    ]

    return any(marker in lowered for marker in forbidden_markers)


def validate_code(code):
    cleaned = _remove_code_fences(code)

    if not cleaned:
        return False, cleaned, "empty response"

    if _contains_reasoning(cleaned):
        return False, cleaned, "LLM returned non-code/reasoning content"

    try:
        tree = ast.parse(cleaned)
    except SyntaxError as error:
        return False, cleaned, f"invalid Python syntax: {error}"

    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if not functions:
        return False, cleaned, "no Python function was generated"

    return True, cleaned, None


def validate_tests(tests):
    cleaned = _remove_code_fences(tests)

    if not cleaned:
        return False, cleaned, "empty response"

    if _contains_reasoning(cleaned):
        return False, cleaned, "LLM returned non-test/reasoning content"

    try:
        tree = ast.parse(cleaned)
    except SyntaxError as error:
        return False, cleaned, f"invalid Python syntax: {error}"

    test_functions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("test_")
    ]

    if not test_functions:
        return False, cleaned, "no pytest test functions were generated"

    imports_solution = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "solution":
                imports_solution = True
                break

    if not imports_solution:
        return False, cleaned, "tests do not import the target from solution"

    return True, cleaned, None