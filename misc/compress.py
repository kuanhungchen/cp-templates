def compress(nums):
    idx2val = sorted(set(nums))
    val2idx = {val: idx for idx, val in enumerate(idx2val)}
    return val2idx, idx2val
