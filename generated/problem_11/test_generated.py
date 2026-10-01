from solution import remove_Occ

def test_char_not_found():
    assert remove_Occ("hello", "x") == "hello"
    assert remove_Occ("", "a") == ""
    assert remove_Occ("abc", "d") == "abc"

def test_single_occurrence():
    assert remove_Occ("hello", "h") == "ello"
    assert remove_Occ("hello", "o") == "hell"
    assert remove_Occ("a", "a") == ""
    assert remove_Occ("abc", "b") == "ac"

def test_multiple_occurrences():
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("abcda", "a") == "bcd"
    assert remove_Occ("PHP", "P") == "H"
    assert remove_Occ("abacada", "a") == "bacad"
    assert remove_Occ("aaaa", "a") == "aa"

def test_two_occurrences():
    assert remove_Occ("aba", "a") == "b"
    assert remove_Occ("abba", "a") == "bb"
    assert remove_Occ("abca", "a") == "bc"

def test_all_same_char():
    assert remove_Occ("aaa", "a") == "a"
    assert remove_Occ("aa", "a") == ""
    assert remove_Occ("a", "a") == ""

def test_empty_string():
    assert remove_Occ("", "a") == ""

def test_case_sensitivity():
    assert remove_Occ("Hello", "h") == "Hello"
    assert remove_Occ("Hello", "H") == "ello"

def test_special_characters():
    assert remove_Occ("a!b!c", "!") == "abc"
    assert remove_Occ("  hello  ", " ") == " hello "