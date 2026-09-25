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


def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def add_one(head):
    head = reverse_list(head)
    curr, last, carry = head, head, 1
    while curr:
        curr.data += carry
        carry, curr.data = divmod(curr.data, 10)
        last = curr
        curr = curr.next
    if carry:
        last.next = Node(carry)
    return reverse_list(head)


digits = [int(d) for d in input().strip()]
head = build_list(digits)
print(to_list(add_one(head)))