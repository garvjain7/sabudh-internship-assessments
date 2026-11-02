class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeTwoLists(list1, list2):
    dummy = tail = ListNode()
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2
    return dummy.next


def build(arr):
    head = None
    for x in reversed(arr):
        head = ListNode(x, head)
    return head


a = list(map(int, input().split()))
b = list(map(int, input().split()))

head = mergeTwoLists(build(a), build(b))

res = []
while head:
    res.append(head.val)
    head = head.next
print(res)