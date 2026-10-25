import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists):
    # min-heap of (value, list index, node); index breaks ties
    heap = [(n.val, i, n) for i, n in enumerate(lists) if n]
    heapq.heapify(heap)
    dummy = cur = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        cur.next = node
        cur = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


def build(arr):
    dummy = cur = ListNode()
    for x in arr:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


print(to_list(merge_k_lists([build([1, 4, 5]), build([1, 3, 4]), build([2, 6])])))
print(to_list(merge_k_lists([])))
print(to_list(merge_k_lists([build([])])))
