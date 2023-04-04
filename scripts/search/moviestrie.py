from pickle import load, dump

# the trie structure per se
# each node saves/has (id, offset) even if it's no used
class TrieNode:
    children: dict[str, 'TrieNode']
    id: int
    offset: int
    def __init__(self):
        self.children = {}
        self.id = 0
        self.offset = 0

# Trie to search for movies
class MoviesTrie:
    root: TrieNode
    filename: str

    def __init__(self, filename: str):
        self.root = TrieNode()
        self.filename = filename

    # add a movie id and its offset in the entity file to the trie
    def add(self, id: int, offset: int):
        node = self.root
        # it creates a string with a 32 (bits) sized binary of the id
        # pads it with zeros to the left if needed and iterate through it
        for bit in format(id, '032b'):
            # create a new node for the bit if not founded
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.id = id
        node.offset = offset

    # search for a movie id in the trie
    def search(self, id: int) -> tuple[int, int]:
        node = self.root
        for bit in format(id, '032b'):
            if bit not in node.children:
                return None
            node = node.children[bit]
        return (node.id, node.offset) if node.id is not None else None

    # save the trie into disk (overwrites already existing file)
    def save(self):
        with open(self.filename, 'wb') as f:
            dump(self.root, f)

    # loads a trie from disk or create a new trie
    @staticmethod
    def load(filename: str) -> 'MoviesTrie':
        trie = MoviesTrie(filename)
        try: 
            with open(filename, 'rb') as f: 
                trie.root = load(f) or TrieNode()
        except: trie.root = TrieNode()
        return trie
