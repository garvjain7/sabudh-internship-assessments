def roman_to_int(s):
    values = {
        "I": 1, "V": 5, "X": 10,
        "L": 50, "C": 100,
        "D": 500, "M": 1000
    }

    result = 0

    for i in range(len(s) - 1):
        if values[s[i]] < values[s[i + 1]]:
            result -= values[s[i]]
        else:
            result += values[s[i]]

    result += values[s[-1]]

    return result


s = input().strip()
print(roman_to_int(s))