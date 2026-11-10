class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def odd_even_list(head):
    if not head or not head.next:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head


vals = list(map(int, input().split()))
dummy = tail = ListNode()
for v in vals:
    tail.next = ListNode(v)
    tail = tail.next
head = odd_even_list(dummy.next)
res = []
while head:
    res.append(head.val)
    head = head.next
print(res)