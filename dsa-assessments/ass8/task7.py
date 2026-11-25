# Problem 7: Rotate a linked list to the right by k places
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


def rotate_right(head, k):
    if head is None or head.next is None:
        return head

    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k %= length
    if k == 0:
        return head

    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None
    tail.next = head
    return new_head


def main():
    values = list(map(int, input("Enter list elements: ").split()))
    k = int(input("Enter k: "))
    head = build_list(values)
    print(list_to_string(rotate_right(head, k)))


if __name__ == "__main__":
    main()
