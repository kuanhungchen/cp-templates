class Node:
    def __init__(self, l, r, val=0, lzy=0, lchd=None, rchd=None):
        self.l = l
        self.r = r
        self.val = val
        self.lzy = lzy
        self.lchd = lchd
        self.rchd = rchd

    def push(self):
        if not self.lchd:
            m = self.l + (self.r - self.l) // 2
            self.lchd = Node(self.l, m)
            self.rchd = Node(m + 1, self.r)
        if self.lzy:
            L = self.r - self.l + 1
            self.lchd.val += self.lzy * (L - L // 2)
            self.lchd.lzy += self.lzy
            self.rchd.val += self.lzy * (L // 2)
            self.rchd.lzy += self.lzy
            self.lzy = 0

class SegTree:
    def __init__(self, n):
        self.FUNC = lambda a, b: a + b
        self.DFLT = 0

        self.root = Node(0, n - 1)

    def ptassign(self, pos, val):
        self.__ptassign(pos, val, self.root)

    def rgadd(self, ql, qr, val):
        # [ql, qr]
        self.__rgadd(ql, qr, val, self.root)

    def query(self, ql, qr):
        # [ql, qr]
        return self.__query(ql, qr, self.root)

    def __ptassign(self, pos, val, node):
        if node.l == node.r:
            node.val = val
            return
        node.push()
        if node.lchd.l <= pos <= node.lchd.r:
            self.__ptassign(pos, val, node.lchd)
        else:
            self.__ptassign(pos, val, node.rchd)
        node.val = self.FUNC(node.lchd.val, node.rchd.val)

    def __rgadd(self, ql, qr, val, node):
        if ql <= node.l and node.r <= qr:
            node.val += val * (node.r - node.l + 1)
            node.lzy += val
            return
        node.push()
        if ql <= node.lchd.r:
            self.__rgadd(ql, qr, val, node.lchd)
        if node.rchd.l <= qr:
            self.__rgadd(ql, qr, val, node.rchd)
        node.val = self.FUNC(node.lchd.val, node.rchd.val)

    def __query(self, ql, qr, node):
        if ql <= node.l and node.r <= qr:
            return node.val
        node.push()
        ans = self.DFLT
        if ql <= node.lchd.r:
            ans = self.FUNC(ans, self.__query(ql, qr, node.lchd))
        if node.rchd.l <= qr:
            ans = self.FUNC(ans, self.__query(ql, qr, node.rchd))
        node.val = self.FUNC(node.lchd.val, node.rchd.val)
        return ans
