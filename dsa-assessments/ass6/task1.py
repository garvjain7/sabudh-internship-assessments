class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


def build_list(values):
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_to_array(head):
    values = []
    while head:
        values.append(head.data)
        head = head.next
    return values


def reverse_list(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def remove_nodes(head):
    head = reverse_list(head)
    dummy = ListNode(0)
    tail = dummy
    max_so_far = float("-inf")
    while head:
        next_node = head.next
        if head.data >= max_so_far:
            max_so_far = head.data
            tail.next = head
            tail = head
        head = next_node
    tail.next = None
    return reverse_list(dummy.next)


head = build_list(list(map(int, input().split())))
print(list_to_array(remove_nodes(head)))
