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


def second_last(head):
    slow, fast = head, head.next
    while fast.next:
        slow, fast = slow.next, fast.next
    return slow.data


values = list(map(int, input().split()))
head = build_list(values)
print(second_last(head))