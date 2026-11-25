# Problem 2: Check if two binary trees are identical
from collections import deque


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def build_tree(tokens):
    """Build a binary tree from level-order tokens. Use "null" for a missing node."""
    if not tokens or tokens[0].lower() in ("null", "n", "#"):
        return None
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    i = 1
    while queue and i < len(tokens):
        node = queue.popleft()
        if i < len(tokens) and tokens[i].lower() not in ("null", "n", "#"):
            node.left = TreeNode(int(tokens[i]))
            queue.append(node.left)
        i += 1
        if i < len(tokens) and tokens[i].lower() not in ("null", "n", "#"):
            node.right = TreeNode(int(tokens[i]))
            queue.append(node.right)
        i += 1
    return root


def are_identical(root1, root2):
    if root1 is None and root2 is None:
        return True
    if root1 is None or root2 is None:
        return False
    return (root1.data == root2.data
            and are_identical(root1.left, root2.left)
            and are_identical(root1.right, root2.right))


def main():
    first = build_tree(input("Enter first tree (level order): ").split())
    second = build_tree(input("Enter second tree (level order): ").split())
    if are_identical(first, second):
        print("Both trees are identical")
    else:
        print("Trees are not identical")


if __name__ == "__main__":
    main()
