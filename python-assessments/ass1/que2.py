# You have been given a string. You need to remove all the duplicates from the string. The final output string should contain each character only once. The respective order of the characters inside the string should remain the same. You can traverse the string only once.
def remove_duplicates(s):
    unique_chars = []
    for char in s:
        if char not in unique_chars:
            unique_chars.append(char)
    return ''.join(unique_chars)

input_string = input()
print(remove_duplicates(input_string))


## Method 2: Using a Set
# Limitation: In set, the order of strings is not preseved
# def remove_duplicates_set(s):
#     return ''.join(set(s))
# input_string = input()
# print(remove_duplicates_set(input_string))