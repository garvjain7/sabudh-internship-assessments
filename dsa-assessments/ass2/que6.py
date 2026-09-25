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


def add_two_numbers(l1, l2):
    l1, l2 = reverse_list(l1), reverse_list(l2)
    dummy = Node(0)
    curr, carry = dummy, 0
    while l1 or l2 or carry:
        s = carry + (l1.data if l1 else 0) + (l2.data if l2 else 0)
        carry, digit = divmod(s, 10)
        curr.next = Node(digit)
        curr = curr.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return reverse_list(dummy.next)


l1 = build_list([int(d) for d in input().strip()])
l2 = build_list([int(d) for d in input().strip()])
print(to_list(add_two_numbers(l1, l2)))