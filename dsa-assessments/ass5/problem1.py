class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next


vals = list(map(int, input().split()))
left, right = int(input()), int(input())
dummy = tail = ListNode()
for v in vals:
    tail.next = ListNode(v)
    tail = tail.next
head = reverse_between(dummy.next, left, right)
res = []
while head:
    res.append(head.val)
    head = head.next
print(res)