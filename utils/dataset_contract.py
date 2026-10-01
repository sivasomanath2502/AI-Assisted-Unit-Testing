import ast


def _first_test_call(problem):
    for test in problem.get("test_list", []):
        tree = ast.parse(test)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                return node

    raise ValueError(
        "Could not infer target function from dataset test_list"
    )


def _value_type(node):
    if isinstance(node, ast.List):
        return "list"

    if isinstance(node, ast.Tuple):
        return "tuple"

    if isinstance(node, ast.Dict):
        return "dictionary"

    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return "string"

        if isinstance(node.value, bool):
            return "boolean"

        if isinstance(node.value, int):
            return "integer"

        if isinstance(node.value, float):
            return "number"

        if node.value is None:
            return "None"

    return "value"


def infer_contract(problem):
    call = _first_test_call(problem)

    return {
        "function_name": call.func.id,
        "argument_count": len(call.args),
        "argument_types": [
            _value_type(arg)
            for arg in call.args
        ],
    }