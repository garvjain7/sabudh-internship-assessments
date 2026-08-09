# Write a program to count the total number of digits in a number using a while loop.
def count_digits(n):
    if n == 0:
        count = 1
    else:
        count = 0
        n = abs(n)
        while n > 0:
            n //= 10
            count += 1
    return count
number = int(input())
print(count_digits(number))