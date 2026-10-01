from solution import sort_matrix

def test_reference_example_1():
    assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]]) == [[1, 1, 1], [1, 2, 3], [2, 4, 5]]

def test_reference_example_2():
    assert sort_matrix([[1, 2, 3], [-2, 4, -5], [1, -1, 1]]) == [[-2, 4, -5], [1, -1, 1], [1, 2, 3]]

def test_reference_example_3():
    assert sort_matrix([[5,8,9],[6,4,3],[2,1,4]]) == [[2, 1, 4], [6, 4, 3], [5, 8, 9]]

def test_empty_matrix():
    assert sort_matrix([]) == []

def test_single_row():
    assert sort_matrix([[1, 2, 3]]) == [[1, 2, 3]]

def test_single_element():
    assert sort_matrix([[5]]) == [[5]]

def test_already_sorted():
    assert sort_matrix([[1, 1, 1], [1, 2, 3], [2, 4, 5]]) == [[1, 1, 1], [1, 2, 3], [2, 4, 5]]

def test_reverse_sorted():
    assert sort_matrix([[2, 4, 5], [1, 2, 3], [1, 1, 1]]) == [[1, 1, 1], [1, 2, 3], [2, 4, 5]]

def test_same_row_sums():
    assert sort_matrix([[1, 2], [2, 1], [3, 0]]) == [[1, 2], [2, 1], [3, 0]]

def test_all_zeros():
    assert sort_matrix([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]

def test_negative_numbers():
    assert sort_matrix([[-1, -2], [-3, -4], [1, 1]]) == [[-3, -4], [-1, -2], [1, 1]]

def test_single_column():
    assert sort_matrix([[3], [1], [2]]) == [[1], [2], [3]]

def test_mixed_positive_negative():
    assert sort_matrix([[10, -5], [-10, 5], [0, 0]]) == [[-10, 5], [0, 0], [10, -5]]

def test_large_values():
    assert sort_matrix([[1000, 2000], [1, 2], [500, 500]]) == [[1, 2], [500, 500], [1000, 2000]]