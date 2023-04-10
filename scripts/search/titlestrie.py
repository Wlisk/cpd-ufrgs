# module imports
# module to serialize and deserialize objects
from pickle import dump, load    

# Define the TrieNode class
class TrieNode:
    children: dict[str, 'TrieNode']
    is_end_of_word: bool
    movies: list[tuple[int, str]]

    # Initialize the Trie
    def __init__(self):
        # Create a dictionary to store child nodes
        self.children = {}
        # Initialize the end-of-word flag to False
        self.is_end_of_word = False
        # Create a list to store the movies at the node
        self.movies = []

#--------------------------------------------------------------------#
# Define the Trie class
class TitlesTrie:
    root: TrieNode
    filename: str

    # Initialize the Trie
    def __init__(self, filename: str):
        # Create a root node for the Trie
        self.root       = TrieNode()
        self.filename   = filename

    # Define the insert function to insert words into the Trie
    def add(self, id: int, title: str):
        # Start at the root node
        node = self.root
        # Split the movie title into words
        words = title.split(" ")
        # For each word in the movie title
        for word in words:
            # Insert the word into the Trie
            # For each character in the word
            for char in word:
                # If the character is not a child node
                if char not in node.children:
                    # Create a new TrieNode for the character
                    node.children[char] = TrieNode()
                # Move down the Trie
                node = node.children[char]
            # Mark the end of the word
            node.is_end_of_word = True
            # Add the movie to the node
            node.movies.append((id, title))

    # Define the search function to search for words in the Trie
    def search(self, word) -> list[tuple[int, str]]:
        # Start at the root node
        node = self.root
        # For each character in the word
        for char in word:
            # If the character is not a child node
            if char not in node.children:
                # Return an empty list, as the word is not in the Trie
                return []
            # Move down the Trie
            node = node.children[char]
        # Return the movies at the node
        return node.movies

    # Define the function to save the Trie to a file
    def save(self):
        # Open the file in binary write mode
        with open(self.filename, 'wb') as f:
            # Serialize the Trie and write it to the file
            dump(self.root, f)

    # Define the function to load the Trie from a file
    @staticmethod
    def load(filename: str) -> 'TitlesTrie':
        # create a new Trie instance
        trie = TitlesTrie(filename)
        # Open the file in binary read mode
        try: 
            with open(filename, 'rb') as f: 
                # load the Trie from the file 
                # or (if error occur loading None) set to default 
                trie.root = load(f) or TrieNode()
        # otherwise create a new root for the Trie 
        except: trie.root = TrieNode()
        # Return the loaded Trie
        return trie
