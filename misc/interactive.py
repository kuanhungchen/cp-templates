# It's recommended to use PyPy3-64 in codeforces.

def query(*data):
    if len(data) == 1:
        if isinstance(data[0], list) or isinstance(data[0], tuple):
            print("?", " ".join(map(str, data[0])), flush=True)
        else:
            print("?", data[0], flush=True)
    else:
        print("?", " ".join(map(str, data)), flush=True)

def answer(*data):
    if len(data) == 1:
        if isinstance(data[0], list) or isinstance(data[0], tuple):
            print("!", " ".join(map(str, data[0])), flush=True)
        else:
            print("!", data[0], flush=True)
    else:
        print("!", " ".join(map(str, data)), flush=True)
