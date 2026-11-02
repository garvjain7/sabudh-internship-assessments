class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


def insertAtBeginning(head, value):
    return Node(value, head)


arr = list(map(int, input().split()))
value = int(input())

head = None
for x in reversed(arr):
    head = Node(x, head)

head = insertAtBeginning(head, value)

res = []
while head:
    res.append(str(head.data))
    head = head.next
print("->".join(res))