#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.io.serial import Serial
from scripts.types import CollectionType
from scripts.search.moviestrie import MoviesTrie

def t1():
    genres_stream = Serial('genres', CollectionType)
    genres_stream.open()

    newdata: list[CollectionType] = []

    newdata.append( CollectionType(1, 0, "Richard") )
    newdata.append( CollectionType(2, 32, "Rasputin") )

    genres_stream.write_all(newdata)
    pos = genres_stream._file.seek(0, 2) # 2 - SEEK_END
    print(pos)

    genres_stream.write( CollectionType(3, 80,  "Anneliz") )
    genres_stream.write( CollectionType(4, 110, "Malbruce") )

    #for data in genres_stream.read(pos):
        #print(data)

    #data = genres_stream.read_all()
    #print(data)

    data = genres_stream.read_last()
    print(data)

    genres_stream.close()

#t1()

def t2():
    trie = MoviesTrie.load("trie.pickle")
    # trie.add(1, 5678)
    # trie.add(35, 8)
    # trie.add(5, 842)
    # trie.add(16, 21)
    # trie.add(9, 9)

    result = trie.search(9)
    if result is not None: print("Found item:", result)
    else: print("Item not found")
    result = trie.search(1)
    if result is not None: print("Found item:", result)
    else: print("Item not found")
    result = trie.search(89)
    if result is not None: print("Found item:", result)
    else: print("Item not found")


    trie.save("trie.pickle")

    #trie = 

t2()

# block_size % item_size = items_per_block