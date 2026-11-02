class SparseVector:
    def __init__(self, nums):
        self.data = {i: v for i, v in enumerate(nums) if v != 0}

    def dotProduct(self, vec):
        a, b = self.data, vec.data
        if len(a) > len(b):
            a, b = b, a
        res = 0
        for i, v in a.items():
            if i in b:
                res += v * b[i]
        return res


nums1 = list(map(int, input().split()))
nums2 = list(map(int, input().split()))

v1 = SparseVector(nums1)
v2 = SparseVector(nums2)
print(v1.dotProduct(v2))