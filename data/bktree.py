from collections import deque

class BKTree:
    def __init__(self, dist_func, items=None):
        self.dist_func = dist_func
        self.root = None
        self.sz = 0

        if items:
            _add = self.add
            for item in items:
                _add(item)

    def add(self, item):
        self.sz += 1
        node = self.root

        if node is None:
            self.root = (item, {})
            return

        _dist_func = self.dist_func

        while True:
            par, chds = node
            dist = _dist_func(item, par)
            node = chds.get(dist)
            if node is None:
                chds[dist] = (item, {})
                break

    def find(self, item, thres):
        """Return (dist, item) whose dist is <= thres from given item. Output
        is not ordered by dist."""
        if self.root is None:
            return []

        ans = []
        cands = deque([self.root])
        _popleft, _extend = cands.popleft, cands.extend
        _append = ans.append
        _dist_func = self.dist_func

        while cands:
            cand, chds = _popleft()
            dist = _dist_func(cand, item)
            if dist <= thres:
                _append((dist, cand))
            if chds:
                _extend(c for d, c in chds.items() if abs(d - dist) <= thres)
        return ans

    def xfind(self, item, thres):
        """Similar to find but yields items lazily. Use find if want a list."""
        if not self.root:
            return

        cands = deque([self.root])
        _popleft, _extend = cands.popleft, cands.extend
        _dist_func = self.dist_func

        while cands:
            cand, chds = _popleft()
            dist = _dist_func(cand, item)
            if dist <= thres:
                yield (dist, cand)
            if chds:
                _extend(c for d, c in chds.items() if abs(d - dist) <= thres)

    def __len__(self):
        return self.sz

    def __iter__(self):
        if self.root is None:
            return

        cands = deque([self.root])
        _popleft, _extend = cands.popleft, cands.extend

        while cands:
            cand, chds = _popleft()
            yield cand
            _extend(chds.values())

    def __repr__(self):
        return ("BKTree(dist_func={}, number of top level nodes={}, "
                "number of total nodes={})").format(
                    self.dist_func.__name__,
                    len(self.root[1]) if self.root is not None else "0",
                    self.sz)
