# Problem 4: Check if every internal node of a BST (given as preorder) has exactly one child


def has_only_one_child(preorder):
    size = len(preorder)
    last = preorder[-1] if size else None

    # If a node has one child, the next element and the last element
    # (the deepest descendant) lie on the same side of it.
    for i in range(size - 1):
        next_is_greater = preorder[i + 1] > preorder[i]
        last_is_greater = last > preorder[i]
        if next_is_greater != last_is_greater:
            return False
    return True


def main():
    preorder = list(map(int, input("Enter preorder traversal (space separated): ").split()))
    print("Yes" if has_only_one_child(preorder) else "No")


if __name__ == "__main__":
    main()
