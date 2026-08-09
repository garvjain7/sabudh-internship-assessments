# Write a program to display only those numbers from a list that satisfy the following conditions:

# The number must be divisible by 5
# If the number is greater than 150, then skip it and move to the next number
# If the number is greater than 500, then stop the loop

def check_numbers(numbers):
    result=[]
    for n in numbers:
        if n > 500:
            break
        if n > 150:
            continue
        if n%5==0:
            result.append(n)
    return result

number_list = list(map(int, input().split(",")))
print(check_numbers(number_list))
