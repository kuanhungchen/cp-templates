class Trie:
    def __init__(self):
        # num of words starting with s, num of words exactly equal to s
        self.root = {'#': 0, '$': 0}

    @property
    def empty(self) -> bool:
        return self.root['#'] == 0

    @property
    def size(self) -> int:
        return self.root["#"]

    def insert(self, word: str):
        node = self.root
        node["#"] += 1
        for c in word:
            if c not in node:
                node[c] = {"#": 0, "$": 0}
            node = node[c]
            node["#"] += 1
        node["$"] += 1

    def delete(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node:
                break
            node = node[c]
        else:
            node = self.root
            node["#"] -= 1
            for c in word:
                node = node[c]
                node["#"] -= 1
            node["$"] -= 1
            return True
        return False

    def search(self, word: str) -> int:
        node = self.root
        for c in word:
            if c not in node or not node["#"]:
                return 0
            node = node[c]
        return node["$"]

    def startsWith(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if c not in node or not node["#"]:
                return 0
            node = node[c]
        return node["#"]
