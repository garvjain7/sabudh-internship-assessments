class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def maxTwinSum(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    prev = None
    while slow:
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt

    ans = 0
    first, second = head, prev
    while second:
        ans = max(ans, first.val + second.val)
        first = first.next
        second = second.next
    return ans


arr = list(map(int, input().split()))

head = None
for x in reversed(arr):
    head = Node(x, head)

print(maxTwinSum(head))