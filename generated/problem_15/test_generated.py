from solution import split_lowerstring

def test_split_at_lowercase():
    assert split_lowerstring("AbCd") == ["bC", "d"]

def test_all_lowercase():
    assert split_lowerstring("Python") == ["y", "t", "h", "o", "n"]

def test_all_lowercase_long():
    assert split_lowerstring("Programming") == ["r", "o", "g", "r", "a", "m", "m", "i", "n", "g"]

def test_empty_string():
    assert split_lowerstring("") == [""]

def test_all_uppercase():
    assert split_lowerstring("ABC") == ["", "", "", ""]

def test_single_lowercase():
    assert split_lowerstring("a") == ["", ""]

def test_single_uppercase():
    assert split_lowerstring("A") == ["A"]

def test_mixed_case():
    assert split_lowerstring("AbC") == ["b", ""]

def test_consecutive_lowercase():
    assert split_lowerstring("abc") == ["", "", "", ""]

def test_consecutive_uppercase():
    assert split_lowerstring("ABC") == ["", "", "", ""]

def test_uppercase_lowercase():
    assert split_lowerstring("Aa") == ["a", ""]

def test_lowercase_uppercase():
    assert split_lowerstring("aA") == ["", "A"]

def test_numbers():
    assert split_lowerstring("a1b") == ["", "1", ""]

def test_special_chars():
    assert split_lowerstring("a!b") == ["", "!", ""]

def test_whitespace():
    assert split_lowerstring("a b") == ["", " ", ""]

def test_numbers_uppercase():
    assert split_lowerstring("1A2B") == ["1", "2", ""]

def test_mixed_alphanumeric():
    assert split_lowerstring("A1bC2") == ["1", "2", ""]

def test_longer_string():
    assert split_lowerstring("HelloWorld") == ["ello", "orld", ""]

def test_all_lowercase_mixed():
    assert split_lowerstring("hELLO") == ["", "E", "L", "L", "O", ""]

def test_uppercase_lowercase_uppercase():
    assert split_lowerstring("AaA") == ["a", ""]