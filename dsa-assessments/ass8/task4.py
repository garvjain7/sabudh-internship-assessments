# Problem 4: Check if a binary tree is a SumTree
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


def check_sum_tree(node):
    """Return (is_sum_tree, total_sum_of_subtree)."""
    if node is None:
        return True, 0
    if node.left is None and node.right is None:
        return True, node.data

    left_ok, left_sum = check_sum_tree(node.left)
    right_ok, right_sum = check_sum_tree(node.right)

    is_valid = left_ok and right_ok and node.data == left_sum + right_sum
    return is_valid, node.data + left_sum + right_sum


def is_sum_tree(root):
    return check_sum_tree(root)[0]


def main():
    root = build_tree(input("Enter tree in level order (use null for empty): ").split())
    if is_sum_tree(root):
        print("The given tree is a SumTree")
    else:
        print("The given tree is not a SumTree")


if __name__ == "__main__":
    main()
