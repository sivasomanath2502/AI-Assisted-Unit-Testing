from solution import remove_Occ

def test_remove_Occ_char_falsy():
    assert remove_Occ("hello", "") == "hello"
    assert remove_Occ("hello", None) == "hello"

def test_remove_Occ_char_not_found():
    assert remove_Occ("hello", "z") == "hello"
    assert remove_Occ("", "a") == ""
    assert remove_Occ("xyz", "") == "xyz"

def test_remove_Occ_single_occurrence():
    assert remove_Occ("abcd", "b") == "acd"
    assert remove_Occ("hello", "h") == "ello"
    assert remove_Occ("hello", "o") == "hell"
    assert remove_Occ("x", "x") == ""

def test_remove_Occ_two_occurrences():
    assert remove_Occ("hello", "l") == "heo"
    assert remove_Occ("abcda", "a") == "bcd"
    assert remove_Occ("aa", "a") == ""
    assert remove_Occ("aba", "a") == "b"

def test_remove_Occ_multiple_occurrences():
    assert remove_Occ("abaca", "a") == "bac"
    assert remove_Occ("aaabaaa", "a") == "aabaa"
    assert remove_Occ("aabbaa", "a") == "abba"