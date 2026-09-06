def max_product_triplet(arr):
    arr.sort()
    n = len(arr)

    product1 = arr[0] * arr[1] * arr[n - 1]
    product2 = arr[n - 3] * arr[n - 2] * arr[n - 1]

    if product1 > product2:
        return arr[0], arr[1], arr[n - 1]
    return arr[n - 3], arr[n - 2], arr[n - 1]


arr = list(map(int, input().replace(",", " ").split()))
result = max_product_triplet(arr)
print(result)