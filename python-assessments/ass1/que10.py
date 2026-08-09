# Define a function that counts vowels and consonants in a word. Assume the input contains only alphabetic characters. The program should correctly handle both uppercase and lowercase letters while counting vowels and consonants.
def count_vowels_consonants(word):
    vowels = 0
    consonants = 0
    word = word.lower()
    for char in word:
        if char in "aeiou":
            vowels += 1
        else:
            consonants += 1
    return vowels, consonants

word = input()
vowels, consonants = count_vowels_consonants(word)
print("Vowels:", vowels)
print("Consonants:", consonants)