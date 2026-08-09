# Write a program to reverse given numbers without slicing. Input will be a positive integer.
def reverse(n):
    result=0
    while n > 0:
        digit=n%10
        result=(result * 10) + digit
        n//=10
    return result
n = int(input())
print(reverse(n))
