# type imports
from scripts.io.iobase  import IOBase
from scripts.types      import BlockHeaderType, BlockType
# module imports 
from struct             import calcsize, pack, unpack, pack_into
from scripts.utils      import \
    get_filename, u32list_to_bytes, bytes_to_u32list
# const imports
from io                 import SEEK_END
from scripts.config     import BLOCK_SIGNATURE, INT_SIZE, BLOCK_BUFFER
from scripts.io.controls import HEADER_BLOCK

# tools for read/write entity/blocks files based on blocks
class Blocks(IOBase):
    _headerdata: BlockHeaderType    # the data of the header
    _classtype: BlockType           # utility to create class instances

    # receives only the name of the entity/blocks file
    def __init__(self, entity_name: str):
        super().__init__(entity_name)
        self._header        = HEADER_BLOCK
        self._headerdata    = BlockHeaderType(0)
        self._filename      = get_filename(entity_name, 'blocks')
        self._classtype     = BlockType

    # verifies if the block signature is a valid block signature
    def is_valid_block(self, block: BlockType) -> bool:
        return block.block_signature == BLOCK_SIGNATURE
    
    # read a block at a given position in the file and load it to memory
    def read(self, block_pos: int) -> BlockType:
        # get the block from disk (size of block_size)
        buffer = super().read_at(block_pos, self._headerdata.block_size)
        # get the format for the block, except the data section
        _format = BlockType.get_format()
        # get the size in bytes occupied by the block, except data section
        offset = calcsize(_format)
        # convert the binary into (BlockType), except data section
        block = BlockType.make( unpack(_format, buffer[:offset]) )
        # get the size in bytes occupied by the data section items
        size = block.num_items * INT_SIZE
        # get the data section items (kept in binary)
        block.data = buffer[offset:offset+size]

        # if there is no error with the pos or the data
        # then maybe we have read a valid block
        return block if self.is_valid_block(block) else None
    
    # write a block into a given position in the file
    def write(self, block_pos: int, block: BlockType):
        # convert the block into a tuple so we can pack it
        bt_block = block.to_bytestuple()
        # get the block format, except for the data section
        _format = BlockType.get_format()
        # write at the given pos the block (binary converted)
        super().write_at(\
            block_pos, \
            pack(f'{_format}{len(block.data)}s', *bt_block) \
        )

    # create a new block at the end of the file 
    # and return the new block position
    def create(self) -> int:
        # update the header with the new num of blocks
        self._headerdata.num_blocks += 1

        # create a new block with default data
        # and convert it to tuple so it can be easily packed
        block = BlockType.new(self._headerdata.num_blocks)
        bt_block = block.to_bytestuple()

        # create an empty bytearray with the size of the block
        bin_block = bytearray(BLOCK_BUFFER) 
        # get the format of the block, except for the data section
        _format = BlockType.get_format()

        # pack the block default info into the buffer
        pack_into(f'{_format}s', bin_block, 0, *bt_block)

        # go to the end of the file and get its absolute position 
        pos = self._file.seek(0, SEEK_END)
        # write the binary block at the given position
        super().write_at(pos, bin_block)

        # return the pos of the new block
        return pos

    # write a list of integers into a block and then 
    # write the block into its blocks file
    def write_into(self, block_pos: int, block: BlockType, _list: list[int]):
        # convert the list into its binary representation
        bin_u32list = u32list_to_bytes(_list)

        # update the data in the block
        block.num_items += len(_list)
        block.end_data += len(bin_u32list)

        # concatenates the old and the new data (both binary)
        block.data += bin_u32list
        
        # finally write the block into the blocks file at the given pos
        self.write(block_pos, block)

    # read only the data of the block at the given position
    def read_data(self, block_pos: int) -> list[int]:
        block: BlockType = self.read(block_pos)
        if block is None: return []
        return bytes_to_u32list(block.data, block.num_items)


