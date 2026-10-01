from utils.persistence import save_generated_artifacts


code = """def example(x):
    return x * 2
"""

tests = """from solution import example

def test_example():
    assert example(5) == 10
"""


artifacts = save_generated_artifacts(
    task_id=999,
    code=code,
    tests=tests,
)

print("Saved artifacts:")
print(artifacts)