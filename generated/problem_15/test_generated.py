from solution import split_lowerstring

def test_split_lowerstring_ab_cd():
    assert split_lowerstring("AbCd") == ["bC", "d"]

def test_split_lowerstring_python():
    assert split_lowerstring("Python") == ["y", "t", "h", "o", "n"]

def test_split_lowerstring_programming():
    assert split_lowerstring("Programming") == ["r", "o", "g", "r", "a", "m", "m", "i", "n", "g"]

def test_empty_string():
    assert split_lowerstring("") == []

def test_single_uppercase():
    assert split_lowerstring("A") == []

def test_single_lowercase():
    assert split_lowerstring("a") == ["a"]

def test_all_uppercase():
    assert split_lowerstring("PYTHON") == ["Y", "T", "H", "O", "N"]

def test_all_lowercase():
    assert split_lowerstring("abc") == ["a", "b", "c"]

def test_starts_with_lowercase():
    assert split_lowerstring("abCde") == ["a", "bC", "d", "e"]

def test_consecutive_lowercase():
    assert split_lowerstring("aBcDe") == ["a", "Bc", "De"]

def test_no_lowercase():
    assert split_lowerstring("ABC") == []

def test_mixed_with_numbers():
    assert split_lowerstring("a1b2C") == ["a1", "b2C"]

def test_start_and_end_with_lowercase():
    assert split_lowerstring("aBCd") == ["a", "BCd"]

def test_trailing_lowercase():
    assert split_lowerstring("Abc") == ["A", "bc"]

def test_leading_lowercase():
    assert split_lowerstring("aBC") == ["a", "BC"]