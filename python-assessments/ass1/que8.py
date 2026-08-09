# Write a Python program to find the median of three values. Median means the middle value after sorting the three numbers.
def median(a, b, c):
    numbers = [a, b, c]
    numbers.sort()
    return numbers[1]
a=int(input())
b=int(input())
c=int(input())
print(median(a,b,c))
