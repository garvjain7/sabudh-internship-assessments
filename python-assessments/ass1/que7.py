# Write a program to use a loop to display elements from a given list present at an odd index position. Odd index refers to index position (1, 3, 5, …), not odd numbers.
def odd_index_elements(lst):
    result = []
    for i in range(len(lst)):
        if i % 2 != 0:
            result.append(lst[i])
    return result

lst = list(map(int, input().split(",")))
print(odd_index_elements(lst))
