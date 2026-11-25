# Problem 3: Check if a subtree with the given sum exists
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


def has_subtree_with_sum(root, target):
    found = False

    def subtree_sum(node):
        nonlocal found
        if node is None:
            return 0
        total = node.data + subtree_sum(node.left) + subtree_sum(node.right)
        if total == target:
            found = True
        return total

    subtree_sum(root)
    return found


def main():
    root = build_tree(input("Enter tree in level order: ").split())
    target = int(input("Enter sum: "))
    print("Yes" if has_subtree_with_sum(root, target) else "No")


if __name__ == "__main__":
    main()
