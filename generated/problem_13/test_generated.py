from solution import count_common as target_function

def test_empty_list():
    assert target_function([]) == 0

def test_single_element():
    assert target_function(['a']) == 1

def test_all_unique_elements():
    result = target_function(['x', 'y', 'z'])
    assert result == 1

def test_multiple_words_with_max_frequency_pink():
    words = ['red','green','black','pink','black','white','black','eyes','white','black','orange','pink','pink','red','red','white','orange','white','black','pink','green','green','pink','green','pink','white','orange','orange','red']
    assert target_function(words) == 6

def test_all_same_words():
    words = ['apple', 'apple', 'apple', 'apple']
    assert target_function(words) == 4

def test_most_frequent_is_not_first():
    words = ['a', 'b', 'b', 'c', 'c', 'c']
    assert target_function(words) == 3

def test_mixed_frequencies():
    words = ['a', 'a', 'b', 'b', 'c', 'c', 'd']
    assert target_function(words) == 2