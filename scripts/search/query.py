import pickle                                                                   # Import the pickle module to serialize and deserialize objects

class TrieNode:                                                                 # Define the TrieNode class
    def __init__(self):                                                         # Initialize the Trie
        self.children = {}                                                      # Create a dictionary to store child nodes
        self.is_end_of_word = False                                             # Initialize the end-of-word flag to False
        self.movies = []                                                        # Create a list to store the movies at the node

class Trie:                                                                     # Define the Trie class
    def __init__(self):                                                         # Initialize the Trie
        self.root = TrieNode()                                                  # Create a root node for the Trie

    def insert(self, word, movie_id, movie_name):                               # Define the insert function to insert words into the Trie
        node = self.root                                                        # Start at the root node
        for char in word:                                                       # For each character in the word
            if char not in node.children:                                       # If the character is not a child node
                node.children[char] = TrieNode()                                # Create a new TrieNode for the character
            node = node.children[char]                                          # Move down the Trie
        node.is_end_of_word = True                                              # Mark the end of the word
        node.movies.append((movie_id, movie_name))                              # Add the movie to the node

    def search(self, word):                                                     # Define the search function to search for words in the Trie
        node = self.root                                                        # Start at the root node
        for char in word:                                                       # For each character in the word
            if char not in node.children:                                       # If the character is not a child node
                return []                                                       # Return an empty list, as the word is not in the Trie
            node = node.children[char]                                          # Move down the Trie
        return sorted(node.movies)                                              # Return the movies at the node in sorted order

def save_trie(trie, filename):                                                  # Define the function to save the Trie to a file
    with open(filename, 'wb') as f:                                             # Open the file in binary write mode
        pickle.dump(trie, f)                                                    # Serialize the Trie and write it to the file

def load_trie(filename):                                                        # Define the function to load the Trie from a file
    with open(filename, 'rb') as f:                                             # Open the file in binary read mode
        trie = pickle.load(f)                                                   # Deserialize the Trie from the file
    return trie                                                                 # Return the loaded Trie

def main():                                                                     # Define the main function
    trie = Trie()                                                               # Create a new Trie object
    with open("Movies.bin", "r", encoding="utf8") as f:                         # Open the movies file in read mode
        for line in f:                                                          # For each line in the file
            line = line.strip()                                                 # Remove any leading/trailing white space
            fields = line.split(";")                                            # Split the line into fields
            if len(fields) >= 3:                                                # If there are at least 3 fields
                movie_id = fields[0]                                            # Get the movie ID
                movie_name = fields[2]                                          # Get the movie name
                words = movie_name.split(" ")                                   # Split the movie name into words
                for word in words:                                              # For each word in the movie name
                    trie.insert(word.lower(), movie_id, movie_name)             # Insert the word into the Trie

    save_trie(trie, 'movies_trie.bin')                                          # Save the Trie to a file
    print('Trie saved to movies_trie.bin')                                      # Print a confirmation message
                        
    loaded_trie = load_trie('movies_trie.bin')                                  # Load the Trie from the file
    print('Trie loaded from movies_trie.bin')                                   # Print a confirmation message
                            
    while True:
        print('\n----------')  
        query = input("Enter a word to search for movies (or 'q' to quit):")    # Ask the user for a word to search for movies or to quit
        if query == "q":                                                        # If the user enters 'q', exit the loop
            break
        result = loaded_trie.search(query.lower())                              # Search for movies that match the user's query using a pre-loaded trie 
        print()
        for movie_id, movie_name in result:
            print(f'ID: {movie_id}  Name: {movie_name}')                        # Print the ID and name of each movie that matches the user's query

if __name__ == "__main__":
    main()
