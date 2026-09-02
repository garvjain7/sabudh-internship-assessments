def multiply_items(numbers):
    product = 1

    for number in numbers:
        product *= number

    return product


def find_largest(numbers):
    return max(numbers)


def find_smallest(numbers):
    return min(numbers)


def remove_duplicates(numbers):
    return list(dict.fromkeys(numbers))


def check_empty(numbers):
    return len(numbers) == 0


def find_largest_odd(numbers):
    odd_numbers = [number for number in numbers if number % 2 != 0]
    return max(odd_numbers) if odd_numbers else None


def remove_required_indexes(numbers):
    result = numbers.copy()

    for index in sorted((0, 4, 5), reverse=True):
        if index < len(result):
            result.pop(index)

    return result


def sort_tuples_by_last_element(tuples):
    return sorted(tuples, key=lambda item: item[-1])


def count_lowercase_letters(words):
    return sum(character.islower() for word in words for character in word)


def extract_exact_consecutive(numbers, k):
    result = []
    index = 0

    while index < len(numbers):
        next_index = index + 1

        while (next_index < len(numbers)
               and numbers[next_index] == numbers[index]):
            next_index += 1

        if next_index - index == k:
            result.append(numbers[index])

        index = next_index

    return result


if __name__ == "__main__":

    # Part A
    numbers = list(map(int, input("Enter integers: ").split()))

    if check_empty(numbers):
        print("5. True")
    else:
        print("1.", multiply_items(numbers))
        print("2.", find_largest(numbers))
        print("3.", find_smallest(numbers))
        print("4.", remove_duplicates(numbers))
        print("5.", False)

        largest_odd = find_largest_odd(numbers)
        print("6.", largest_odd if largest_odd is not None
              else "No odd numbers found")

        print("7.", remove_required_indexes(numbers))

    # Part B
    tuple_count = int(input("Enter number of tuples: "))
    tuples = []

    for _ in range(tuple_count):
        tuples.append(tuple(map(int, input("Enter tuple elements: ").split())))

    print("8.", sort_tuples_by_last_element(tuples))

    # Part C
    words = input("Enter words: ").split()
    print("9.", count_lowercase_letters(words))

    # Part D
    numbers = list(map(int, input("Enter integers: ").split()))
    k = int(input("Enter k: "))

    print("10.", extract_exact_consecutive(numbers, k))