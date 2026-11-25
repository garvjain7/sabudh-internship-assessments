# Problem 6: Delete the last occurrence of an item from a linked list
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


def delete_last_occurrence(head, key):
    last_match = None
    before_last_match = None
    prev, curr = None, head

    while curr:
        if curr.data == key:
            last_match = curr
            before_last_match = prev
        prev, curr = curr, curr.next

    if last_match is None:
        return head
    if before_last_match is None:
        return head.next
    before_last_match.next = last_match.next
    return head


def main():
    values = list(map(int, input("Enter list elements: ").split()))
    key = int(input("Enter item to delete: "))
    head = build_list(values)
    print("Created Linked list:", list_to_string(head))
    head = delete_last_occurrence(head, key)
    print(f"List after deletion of {key}:", list_to_string(head))


if __name__ == "__main__":
    main()
