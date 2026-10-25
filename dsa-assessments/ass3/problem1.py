def product_except_self(nums):
    n = len(nums)
    res = [1] * n
    p = 1
    # prefix products
    for i in range(n):
        res[i] = p
        p *= nums[i]
    s = 1
    # suffix products
    for i in range(n - 1, -1, -1):
        res[i] *= s
        s *= nums[i]
    return res


print(product_except_self([1, 2, 3, 4]))
print(product_except_self([-1, 1, 0, -3, 3]))
