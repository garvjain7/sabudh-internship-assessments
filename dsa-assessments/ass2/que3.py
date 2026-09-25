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


def remove_duplicates(head):
    curr = head
    while curr and curr.next:
        if curr.data == curr.next.data:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return head


values = list(map(int, input().split()))
head = build_list(values)
print(to_list(remove_duplicates(head)))