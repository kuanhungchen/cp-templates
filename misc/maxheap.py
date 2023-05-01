from heapq import _siftup_max, _siftdown_max, _heapify_max

def heappop_max(pq):
    ans = pq.pop()
    if pq:
        ans, pq[0] = pq[0], ans
        _siftup_max(pq, 0)
    return ans

def heapreplace_max(pq, x):
    ans, pq[0] = pq[0], x
    _siftup_max(pq, 0)
    return ans

def heappush_max(pq, x):
    pq.append(x)
    _siftdown_max(pq, 0, len(pq) - 1)

def heappushpop_max(pq, x):
    if pq and pq[0] > x:
        x, pq[0] = pq[0], x
        _siftup_max(pq, 0)
    return x

heapify_max = _heapify_max
