def remove_duplicates(s):
    stack = []
    for ch in s:
        # cancel with top if equal
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


print(remove_duplicates("abbaca"))
print(remove_duplicates("azxxzy"))
