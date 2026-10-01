from solution import count_common
import pytest

def test_empty_list():
    assert count_common([]) == []

def test_single_word():
    assert count_common(['hello']) == [('hello', 1)]

def test_two_distinct_words():
    assert count_common(['a', 'b']) == [('a', 1), ('b', 1)]

def test_three_distinct_words():
    assert count_common(['a', 'b', 'c']) == [('a', 1), ('b', 1), ('c', 1)]

def test_four_distinct_words():
    assert count_common(['a', 'b', 'c', 'd']) == [('a', 1), ('b', 1), ('c', 1), ('d', 1)]

def test_more_than_four_distinct_words():
    words = ['a', 'b', 'c', 'd', 'e']
    result = count_common(words)
    assert len(result) == 4
    assert result == [('a', 1), ('b', 1), ('c', 1), ('d', 1)]

def test_example_1():
    words = ['red','green','black','pink','black','white','black','eyes','white','black','orange','pink','pink','red','red','white','orange','white','black','pink','green','green','pink','green','pink','white','orange','orange','red']
    expected = [('pink', 6), ('black', 5), ('white', 5), ('red', 4)]
    assert count_common(words) == expected

def test_example_2():
    words = ['one', 'two', 'three', 'four', 'five', 'one', 'two', 'one', 'three', 'one']
    expected = [('one', 4), ('two', 2), ('three', 2), ('four', 1)]
    assert count_common(words) == expected

def test_example_3():
    words = ['Facebook', 'Apple', 'Amazon', 'Netflix', 'Google', 'Apple', 'Netflix', 'Amazon']
    expected = [('Apple', 2), ('Amazon', 2), ('Netflix', 2), ('Facebook', 1)]
    assert count_common(words) == expected

def test_tie_breaking_by_first_appearance():
    # Words with same count should appear in order of first appearance
    words = ['x', 'y', 'z', 'x', 'y', 'z']  # each appears twice, order x, y, z
    expected = [('x', 2), ('y', 2), ('z', 2)]
    assert count_common(words) == expected

def test_tie_breaking_with_more_than_four():
    # Only top 4 should be returned, ties beyond 4 are dropped
    words = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']  # each twice
    result = count_common(words)
    assert len(result) == 4
    assert result == [('a', 2), ('b', 2), ('c', 2), ('d', 2)]

def test_case_sensitivity():
    words = ['Apple', 'apple', 'Apple']
    expected = [('Apple', 2), ('apple', 1)]
    assert count_common(words) == expected

def test_non_string_elements():
    # The function doesn't restrict to strings, but we test with mixed types
    words = [1, 2, 1, 3, 2, 1]
    expected = [(1, 3), (2, 2), (3, 1)]
    assert count_common(words) == expected

def test_large_counts():
    words = ['a'] * 100 + ['b'] * 50 + ['c'] * 25 + ['d'] * 10 + ['e'] * 5
    expected = [('a', 100), ('b', 50), ('c', 25), ('d', 10)]
    assert count_common(words) == expected

def test_all_same_word():
    words = ['same'] * 10
    assert count_common(words) == [('same', 10)]

def test_return_type():
    result = count_common(['a', 'b'])
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2
        assert isinstance(item[0], str)
        assert isinstance(item[1], int)