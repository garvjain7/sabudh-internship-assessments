# Problem 1: Maximum depth of a binary tree
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


def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def main():
    tokens = input("Enter tree in level order (use null for empty): ").split()
    root = build_tree(tokens)
    print("Maximum depth of tree is", max_depth(root))


if __name__ == "__main__":
    main()
