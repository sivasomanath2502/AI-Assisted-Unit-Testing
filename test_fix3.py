from utils.artifact_validator import validate_tests


print("=" * 60)
print("CASE 1: test_duplicate WITHOUT alias")
print("=" * 60)

bad_tests = """
from solution import test_duplicate

def test_duplicates():
    assert test_duplicate([1, 2, 2]) == True
"""

valid, cleaned, error = validate_tests(
    bad_tests,
    required_function_name="test_duplicate",
)

print("Valid:", valid)
print("Error:", error)


print("\n" + "=" * 60)
print("CASE 2: test_duplicate WITH alias")
print("=" * 60)

good_tests = """
from solution import test_duplicate as target_function

def test_duplicates():
    assert target_function([1, 2, 2]) == True
"""

valid, cleaned, error = validate_tests(
    good_tests,
    required_function_name="test_duplicate",
)

print("Valid:", valid)
print("Error:", error)