# type import
from scripts.types                      import CollectionType, BlockType
from scripts.io.serial                  import Serial
from scripts.io.blocks                  import Blocks
# module imports
from scripts.search.controls            import found_in_entity, by_name

# add to or create entities file or blocks files
# receives a list o tuples data contains a dict, 
# a blocks file stream and a entity file stream
def generate_blocks(collections: list[tuple[dict[str, list[int]], Blocks, Serial]]):
    # loop through the collections
    for collection in collections:
        # _dict:dict[str|int, list[int]], _block:Blocks, _stream:Serial
        _dict, _block, _stream = collection

        _stream.open()
        _block.open()

        # id's are based on the num of elements in the entities file
        idx: int = _stream._headerdata.num_items + 1

        # read all items from the entity file
        entity_data: list[CollectionType] = _stream.read_all()

        # loop through each collection item found 
        for item in _dict.keys():
            # initialize the pos to start after the header data (default)
            block_pos = _block._header.struct_size

            # check if the item is already in the entitity file
            # if it is not, create a new block for the item
            found: CollectionType = \
                found_in_entity(entity_data, item, by_name)
            
            if found is None: 
                # create a new block in the blocks file for this new item
                block_pos: int = _block.create()

                # write the new item into the entity file
                _stream.write( \
                    CollectionType(idx, block_pos, bytes(item, 'utf-8')) \
                )
                # update the id for the new items to come
                idx += 1
                print(f'Creating new block for [{item}]')

            else: 
                block_pos = found.block_pos
                print(f'Block for [{item}] already exists')

            # print(block_pos, sep='\n')
            item_block: BlockType = _block.read(block_pos)

            # add a list of integers into the block
            # if there is new elements (IDs)
            _len: int = len(_dict[item])
            if _len: 
                _block.write_into(block_pos, item_block, _dict[item])
                print(f'({_len}) elements were written into [{item}] block')
                
        _stream.close()
        _block.close()
