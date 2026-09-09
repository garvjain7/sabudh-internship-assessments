import numpy as np


def create_1d_array():
    return np.random.randint(0, 100, 10)


def create_2d_array():
    return np.random.randint(-10, 11, size=(3, 4))


def flatten_array(arr):
    return arr.flatten()


def create_modified_copy(arr):
    arr_copy = arr.copy()
    arr_copy[0] = -1
    return arr_copy


def slice_every_second(arr):
    return arr[::2]


def get_third_element(arr):
    return arr[2]


def get_last_element(arr):
    return arr[2, 3]


def get_submatrix(arr):
    return arr[:2, 2:]


def get_second_row(arr):
    return arr[1, :]


def get_first_column(arr):
    return arr[:, 0]


def create_range_array():
    return np.arange(1, 11)


def add_arrays(a, d):
    return a + d


def multiply_array(b):
    return b * 2


def matrix_multiply(b, b_double):
    return b @ b_double.T


def calculate_means(a, b, b_double):
    return np.array([np.mean(a), np.mean(b), np.mean(b_double)])


def calculate_sum(a):
    return np.sum(a)


def find_min(b):
    return np.min(b)


def find_max(b_double):
    return np.max(b_double)


if __name__ == "__main__":
    a = create_1d_array()
    print("1.1 a:", a)

    b = create_2d_array()
    print("1.2 b:\n", b)

    b_flat = flatten_array(b)
    print("1.3 b_flat:", b_flat)

    a_copy = create_modified_copy(a)
    print("1.4 a_copy:", a_copy)

    c = slice_every_second(a)
    print("1.5 c:", c)

    print("2.1 Third element of a:", get_third_element(a))
    print("2.2 Last element of b:", get_last_element(b))
    print("2.3 Submatrix of b:\n", get_submatrix(b))

    b_row = get_second_row(b)
    print("2.4 b_row:", b_row)

    b_col = get_first_column(b)
    print("2.5 b_col:", b_col)

    d = create_range_array()
    print("3.1 d:", d)

    e = add_arrays(a, d)
    print("3.2 e:", e)

    b_double = multiply_array(b)
    print("3.3 b_double:\n", b_double)

    f = matrix_multiply(b, b_double)
    print("3.4 f:\n", f)

    g = calculate_means(a, b, b_double)
    print("3.5 g:", g)

    print("4.1 a_sum:", calculate_sum(a))
    print("4.2 b_min:", find_min(b))
    print("4.3 b_double_max:", find_max(b_double))
