def sort_by_value(dictionary, reverse=False):
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse))


def iterate_keys(dictionary):
    result = []
    for key in dictionary:
        result.append(key)
    return result


def iterate_values(dictionary):
    result = []
    for value in dictionary.values():
        result.append(value)
    return result


def iterate_items(dictionary):
    result = []
    for key, value in dictionary.items():
        result.append((key, value))
    return result


def merge_dictionaries(first, second):
    return {**first, **second}


def calculate_sum(dictionary):
    return sum(dictionary.values())


def calculate_product(dictionary):
    if not dictionary:
        return None

    product = 1
    for value in dictionary.values():
        product *= value
    return product


def sort_by_key(dictionary):
    return dict(sorted(dictionary.items()))


def remove_duplicate_values(dictionary):
    result = {}

    for key, value in dictionary.items():
        if value not in result.values():
            result[key] = value

    return result


def read_dictionary():
    dictionary = {}
    count = int(input("Enter number of key-value pairs: "))

    for _ in range(count):
        key = input("Enter key: ")
        value = float(input("Enter value: "))
        dictionary[key] = value

    return dictionary


if __name__ == "__main__":
    dictionary = read_dictionary()

    print("1. Ascending by value:", sort_by_value(dictionary))
    print("1. Descending by value:", sort_by_value(dictionary, True))

    print("2. Keys:", iterate_keys(dictionary))
    print("2. Values:", iterate_values(dictionary))
    print("2. Key-value pairs:", iterate_items(dictionary))

    print("Enter first dictionary for merging:")
    first = read_dictionary()

    print("Enter second dictionary for merging:")
    second = read_dictionary()

    print("3. Merged dictionary:", merge_dictionaries(first, second))

    print("4. Sum:", calculate_sum(dictionary))

    product = calculate_product(dictionary)
    print("4. Product:", product if product is not None else "Dictionary is empty")

    print("5. Sorted by key:", sort_by_key(dictionary))

    print("6. Without duplicate values:",
          remove_duplicate_values(dictionary))