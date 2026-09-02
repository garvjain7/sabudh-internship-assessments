def create_mixed_tuple(integer, decimal, text, boolean):
    return integer, decimal, text, boolean


def create_number_tuple(numbers):
    return tuple(numbers)


def get_specific_element(items, index):
    return items[index]


def get_fourth_from_end(items):
    return items[-4] if len(items) >= 4 else None


def add_item_to_tuple(items, item):
    return items + (item,)


def convert_tuple_to_dictionary(items):
    return dict(enumerate(items))


def replace_last_elements(tuple_list, value):
    return [item[:-1] + (value,) for item in tuple_list]


if __name__ == "__main__":

    # Part A

    integer = int(input("Enter an integer: "))
    decimal = float(input("Enter a float: "))
    text = input("Enter a string: ")
    boolean = input("Enter True or False: ").strip().lower() == "true"

    mixed_tuple = create_mixed_tuple(integer, decimal, text, boolean)
    print("1.", mixed_tuple)

    numbers = list(map(int, input("Enter at least five numbers: ").split()))
    number_tuple = create_number_tuple(numbers)

    index = int(input("Enter the index to print: "))

    if 0 <= index < len(number_tuple):
        print("2.", get_specific_element(number_tuple, index))
    else:
        print("2. Invalid index")

    items = tuple(input("Enter tuple elements: ").split())
    fourth = get_fourth_from_end(items)

    if fourth is None:
        print("3. Tuple contains fewer than 4 elements")
    else:
        print("3.", fourth)

    # Part B

    item = input("Enter an item to add: ")
    updated_tuple = add_item_to_tuple(items, item)

    print("4. Original:", items)
    print("4. Updated:", updated_tuple)

    # Part C

    values = tuple(input("Enter tuple elements for dictionary conversion: ").split())
    print("5.", convert_tuple_to_dictionary(values))

    # Part D

    tuple_count = int(input("Enter number of tuples: "))
    tuple_list = []

    for _ in range(tuple_count):
        values = tuple(map(int, input("Enter tuple elements: ").split()))
        tuple_list.append(values)

    print("6.", replace_last_elements(tuple_list, 100))