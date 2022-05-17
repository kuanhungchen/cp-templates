from sys            import stdin,  stderr, stdout, setrecursionlimit
from bisect         import bisect_left, bisect_right
from collections    import defaultdict, deque, Counter
from itertools      import accumulate, combinations, permutations, product
from functools      import lru_cache, cmp_to_key, reduce
from heapq          import heapify, heappush, heappop, heappushpop, heapreplace
# from pypyjit        import set_param
# set_param("max_unroll_recursion=-1")
# setrecursionlimit(300005)
INF   = 1 << 60
MOD   = 998244353 + 1755654
input = lambda: stdin.readline().rstrip("\r\n")
dbg   = lambda *A, **M: stderr.write("\033[91m" + \
        M.get("sep", " ").join(map(str, A)) + M.get("end", "\n") + "\033[0m")
# ============================ START OF MY CODE ============================ #

def solve(_tc):
    pass


if __name__ == "__main__":
    _tcs = int(input())
    for _tc in range(1, vars().get("_tcs", 1) + 1):
        dbg("=== Case {} ===".format(str(_tc).rjust(2)))
        solve(_tc)
