def heappop_max(hp):
    ans = hp.pop()
    if hp:
        ans, hp[0] = hp[0], ans
        heapq._siftup_max(hp, 0)
    return ans

def heapreplace_max(hp, x):
    ans, hp[0] = hp[0], x
    heapq._siftup_max(hp, 0)
    return ans

def heappush_max(hp, x):
    hp.append(x)
    heapq._siftdown_max(hp, 0, len(hp) - 1)

def heappushpop_max(hp, x):
    if hp and hp[0] > x:
        x, hp[0] = hp[0], x
        heapq._siftup_max(hp, 0)
    return x

heapify_max = heapq._heapify_max
