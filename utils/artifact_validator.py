import ast


def _remove_code_fences(text):
    text = text.strip()

    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()

        if len(lines) >= 2:
            text = "\n".join(lines[1:-1]).strip()

    return text


def _contains_reasoning(text):
    lowered = text.lower()

    forbidden = [
        "<think>",
        "</think>",
        "user safety:",
        "here is the code:",
        "here's the code:",
        "here are the tests:",
        "sure, here",
    ]

    return any(
        marker in lowered
        for marker in forbidden
    )


def validate_code(code, required_function_name=None):
    cleaned = _remove_code_fences(code)

    if not cleaned:
        return False, cleaned, "empty response"

    if _contains_reasoning(cleaned):
        return (
            False,
            cleaned,
            "LLM returned non-code/reasoning content",
        )

    try:
        tree = ast.parse(cleaned)

    except SyntaxError as error:
        return (
            False,
            cleaned,
            f"invalid Python syntax: {error}",
        )

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    ]

    if not functions:
        return (
            False,
            cleaned,
            "no Python function was generated",
        )

    if required_function_name:
        names = {
            node.name
            for node in functions
        }

        if required_function_name not in names:
            return (
                False,
                cleaned,
                (
                    f"required function "
                    f"'{required_function_name}' "
                    f"was not generated"
                ),
            )

    return True, cleaned, None


def validate_tests(tests, required_function_name=None):
    cleaned = _remove_code_fences(tests)

    if not cleaned:
        return False, cleaned, "empty response"

    if _contains_reasoning(cleaned):
        return (
            False,
            cleaned,
            "LLM returned non-test/reasoning content",
        )

    try:
        tree = ast.parse(cleaned)

    except SyntaxError as error:
        return (
            False,
            cleaned,
            f"invalid Python syntax: {error}",
        )

    test_functions = [
        node
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.FunctionDef)
            and node.name.startswith("test_")
        )
    ]

    if not test_functions:
        return (
            False,
            cleaned,
            "no pytest test functions were generated",
        )

    imported_names = set()

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == "solution"
        ):
            for alias in node.names:
                imported_names.add(alias.name)

                if (
                    required_function_name
                    and alias.name == required_function_name
                    and required_function_name.startswith("test_")
                    and alias.asname is None
                ):
                    return (
                        False,
                        cleaned,
                        (
                            f"target function "
                            f"'{required_function_name}' "
                            f"must be imported using an alias "
                            f"because its name starts with 'test_'"
                        ),
                    )

    if not imported_names:
        return (
            False,
            cleaned,
            "tests do not import the target from solution",
        )

    if (
        required_function_name
        and required_function_name not in imported_names
    ):
        return (
            False,
            cleaned,
            (
                f"tests do not import required function "
                f"'{required_function_name}'"
            ),
        )

    return True, cleaned, None