class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def build_list(values):
    dummy = Node(0)
    curr = dummy
    for v in values:
        curr.next = Node(v)
        curr = curr.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.data)
        head = head.next
    return out


def delete_middle(head):
    if not head or not head.next:
        return None
    slow, fast, prev = head, head, None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    prev.next = slow.next
    return head


values = list(map(int, input().split()))
head = build_list(values)
print(to_list(delete_middle(head)))