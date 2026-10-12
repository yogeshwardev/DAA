class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def build_bst(data):
    root = None
    for key in data:
        if root is None:
            root = Node(key)
            continue
        cur = root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = Node(key)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(key)
                    break
                cur = cur.right
    return root


def bst_search(root, key):
    comparisons = 0
    cur = root
    while cur is not None:
        comparisons += 1
        if key == cur.key:
            return True, comparisons
        cur = cur.left if key < cur.key else cur.right
    return False, comparisons


def height(root):
    if root is None:
        return 0
    level, h = [root], 0
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c is not None]
    return h
