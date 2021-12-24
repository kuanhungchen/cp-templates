class DisjointSparseTable:
    def __init__(self, nums):
        self.FUNC = FUNC = lambda a, b: a + b

        n = len(nums)
        LOGN = n.bit_length()
        self.lgs = lgs = [0 for _ in range(1 << LOGN)]
        for i in range(2, 1 << LOGN):
            lgs[i] = lgs[i >> 1] + 1

        self.st = st = [[0 for _ in range(n)] for _ in range(LOGN)]
        st[0] = nums[:]
        for depth in range(1, LOGN):
            cur = st[depth]
            shift = 1 << depth
            for l in range(0, n, 2 * shift):
                mid = min(l + shift, n)
                cur[mid - 1] = nums[mid - 1]
                for i in reversed(range(l, mid - 1)):
                    cur[i] = FUNC(nums[i], cur[i + 1])
                if mid == n: break
                r = min(l + 2 * shift, n)
                cur[mid] = nums[mid]
                for i in range(mid + 1, r):
                    cur[i] = FUNC(nums[i], cur[i - 1])

    def query(self, ql, qr):
        # [ql, qr)
        qr -= 1
        if ql == qr: return self.st[0][ql]
        depth = self.lgs[ql ^ qr]
        return self.FUNC(self.st[depth][ql], self.st[depth][qr])
