# Problem 5: Insert a node before the middle of a linked list
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


def build_list(values):
    head = tail = None
    for value in values:
        node = ListNode(value)
        if head is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head


def list_to_string(head):
    parts = []
    while head:
        parts.append(str(head.data))
        head = head.next
    return "->".join(parts) if parts else "Empty list"


def count_nodes(head):
    count = 0
    while head:
        count += 1
        head = head.next
    return count


def insert_before_middle(head, value):
    new_node = ListNode(value)
    length = count_nodes(head)
    middle_position = (length + 1) // 2  # 1-based; first middle when length is even

    # Middle is the head (or the list is empty): new node becomes the head
    if middle_position <= 1:
        new_node.next = head
        return new_node

    prev = head
    for _ in range(middle_position - 2):
        prev = prev.next
    new_node.next = prev.next
    prev.next = new_node
    return head


def main():
    values = list(map(int, input("Enter list elements: ").split()))
    value = int(input("Enter value to insert before middle: "))
    head = build_list(values)
    print(list_to_string(insert_before_middle(head, value)))


if __name__ == "__main__":
    main()
