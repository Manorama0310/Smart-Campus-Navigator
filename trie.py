class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Trie for prefix-based auto-complete."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def starts_with(self, prefix):
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._collect(node, prefix, results)
        return sorted(results)

    def _collect(self, node, current, results):
        if node.is_end:
            # Restore title casing using the known location list in app.py by
            # matching the lowercase string there.
            results.append(current)
        for char, child in node.children.items():
            self._collect(child, current + char, results)
