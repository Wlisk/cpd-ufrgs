# module imports
from pickle import load, dump

# the trie structure per se
# each node saves/has (id, offset) even if it's no used
class TrieNode:
    children: dict[str, 'TrieNode']     # the Trie node (the Trie per se)
    id: int                             # the movie id 
    offset: int                         # the movie pos in the entity file

    def __init__(self):
        self.children   = {}
        self.id         = 0
        self.offset     = 0

# Trie to search for movies
class MoviesTrie:
    root: TrieNode      # the Trie structure
    filename: str       # the filename for the Trie in the disk

    def __init__(self, filename: str):
        self.root       = TrieNode()
        self.filename   = filename

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
        # update the data for this position
        node.id = id
        node.offset = offset

    # search for a movie id in the trie
    def search(self, id: int) -> tuple[int, int]:
        # initialize with the root
        node = self.root
        # it creates a string with a 32 (bits) sized binary of the id
        # pads it with zeros to the left if needed and iterate through it
        for bit in format(id, '032b'):
            # if the bit is not in the node, then the id is not in the node
            if bit not in node.children: return None
            # go to the next 'bit' node
            node = node.children[bit]
        # if all 'bits' matched, then we found our item in the Trie
        return (node.id, node.offset) if node.id is not None else None

    # save the trie into disk (overwrites already existing file)
    def save(self):
        with open(self.filename, 'wb') as f:
            dump(self.root, f)

    # loads a trie from disk or create a new trie
    @staticmethod
    def load(filename: str) -> 'MoviesTrie':
        # create a new Trie instance
        trie = MoviesTrie(filename)
        # tries to load the Trie if it exists
        try: 
            with open(filename, 'rb') as f: 
                # load the Trie from the file 
                # or (if error occur loading None) set to default 
                trie.root = load(f) or TrieNode()
        # otherwise create a new root for the Trie 
        except: trie.root = TrieNode()
        # return the new/loaded Trie
        return trie
