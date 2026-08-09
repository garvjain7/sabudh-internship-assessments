# Read an integer N. For all non-negative integers i < N, print i^2 as a list.
def square(n):
    square_list = []
    for i in range(n):
        square_list.append(i ** 2)
    return square_list
number = int(input())
print(square(number))