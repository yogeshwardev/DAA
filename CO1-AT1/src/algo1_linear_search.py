def linear_search(data, key):
    comparisons = 0
    for i in range(len(data)):
        comparisons += 1
        if data[i] == key:
            return i, comparisons
    return -1, comparisons
