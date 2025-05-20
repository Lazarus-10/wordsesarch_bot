class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self, words=None):
        self.root = TrieNode()
        if words:
            for word in words:
                self.insert(word)

    def insert(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node if node.is_end else None

    def delete(self, s):
        def rec(node, s, i):
            if i == len(s):
                node.is_end = False
                return len(node.children) == 0
            next_deletion = rec(node.children[s[i]], s, i + 1)
            if next_deletion:
                del node.children[s[i]]
            return next_deletion and not node.is_end and len(node.children) == 0

        if self.search(s):
            rec(self.root, s, 0)
            
    def get_strings(self):
        def rec(node, string, strings):
            if node.is_end:
                strings.append("".join(string))
            for ch in node.children:
                string.append(ch)
                rec(node.children[ch], string, strings)
                string.pop()
        strings = []
        rec(self, [], strings)
        return strings