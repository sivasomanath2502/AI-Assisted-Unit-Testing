from solution import find_Volume


def test_reference_examples():
    assert find_Volume(10, 8, 6) == 240
    assert find_Volume(3, 2, 2) == 6
    assert find_Volume(1, 2, 1) == 1


def test_zero_base():
    assert find_Volume(0, 8, 6) == 0


def test_zero_height():
    assert find_Volume(10, 0, 6) == 0


def test_zero_length():
    assert find_Volume(10, 8, 0) == 0


def test_all_zero_dimensions():
    assert find_Volume(0, 0, 0) == 0


def test_odd_product_returns_fractional_volume():
    assert find_Volume(1, 1, 1) == 0.5


def test_float_dimensions():
    assert find_Volume(2.5, 4.0, 6.0) == 30.0
    assert find_Volume(1.5, 2.0, 3.0) == 4.5


def test_mixed_int_and_float_dimensions():
    assert find_Volume(2, 3.0, 4) == 12.0
    assert find_Volume(2.0, 3, 4.0) == 12.0


def test_large_dimensions():
    assert find_Volume(1000, 1000, 1000) == 500000000