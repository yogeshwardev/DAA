def preprocess(data):
    return sorted(data)


def binary_search(arr, key, low=0, high=None, _c=None):
    if high is None:
        high = len(arr) - 1
    if _c is None:
        _c = [0]
    if low > high:
        return -1, _c[0]
    mid = (low + high) // 2
    _c[0] += 1
    if arr[mid] == key:
        return mid, _c[0]
    if key < arr[mid]:
        return binary_search(arr, key, low, mid - 1, _c)
    return binary_search(arr, key, mid + 1, high, _c)


def binary_search_iterative(arr, key):
    low, high, comparisons = 0, len(arr) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        if key < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons
