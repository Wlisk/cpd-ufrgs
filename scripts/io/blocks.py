# type imports
from dataclasses import dataclass, astuple
from scripts.io.iobase import IOBase
from scripts.types import BlockHeaderType, BlockType, EntityInfo

from io import SEEK_END
from scripts.config import BLOCK_SIZE, BLOCK_SIGNATURE
from struct import calcsize, pack, unpack, pack_into
from scripts.binaries.controls import HEADER_BLOCK, BLOCK
from scripts.utils import get_filename, u32list_to_bytes
# 
class Blocks(IOBase):
    _header: EntityInfo
    _headerdata: BlockHeaderType
    _classtype: BlockType

    def __init__(self, entity_name: str):
        super().__init__(entity_name)
        self._header = HEADER_BLOCK
        self._headerdata = BlockHeaderType(0)
        self._filename = get_filename(self._entity.name, 'blocks')
        self._classtype = BlockType

    def open(self):
        super().open()
        if not self._file_exists:
            self._file_exists = True
            super().write_header()
        else:
            self._headerdata = super().read_header()

    # verifies if the block signature is a valid block signature
    def is_valid_block(self, signature: int) -> bool:
        return signature == BLOCK_SIGNATURE

    # create a new block at the end of the file 
    # and return the new block position
    def create(self) -> int:
        pos = self._file.seek(0, SEEK_END)
        block = BlockType.create(self._headerdata.num_blocks + 1)
        bt_block = block.to_bytestuple()
        #print(BLOCK.struct_format, len(bt_block), len(bt_block[-1]))
        # create an empty byte string with the correct length
        bin = bytearray(BLOCK.struct_size) # + len(block.data)
        # pack the BlockType data into the byte string
        #print(*bt_block[:-1])
        pack_into(BlockType.get_format(), bin, 0, *bt_block[:-1])
        # pack the data into the remaining bytes in the byte string
        pack_into(\
            f'{BlockType.get_data_size()}s', bin, \
            calcsize(BlockType.get_format()), bt_block[-1] \
        )
        #bin = pack(BLOCK.struct_format, *bt_block)
        super().write_at(pos, bin)
        self._headerdata.num_blocks += 1
        return pos

    # read a block at a given position in the file
    # and load it to memory
    def read(self, block_pos: int) -> BlockType:
        buffer = super().read_at(block_pos, self._headerdata.block_size)
        block = BlockType.make( 
            unpack(self._header.struct_format, buffer) \
        )
        if not self.is_valid_block(block.block_signature): return None
        return block
    
    # write a block into a given position in the file
    def write(self, block_pos: int, block: BlockType):
        print(self._header.struct_format, block.to_bytestuple())
        bt_block = block.to_bytestuple()
        # bin = bytearray(BLOCK.struct_size)
        # pack_into(BlockType.get_format(), bin, 0, *bt_block[:-1])
        # pack_into(\
        #     f'{BlockType.get_data_size()}s', bin, \
        #     calcsize(BlockType.get_format()), block.data \
        # )
        super().write_at(\
            block_pos, \
            pack(\
                f'{BlockType.get_format()}{len(bt_block[-1])}s', \
                *bt_block \
            ) \
        )

    # write a list of integers into a block and then 
    # write the block into its blocks file
    def write_into(self, block_pos: int, block: BlockType, _list: list[int]):
        # convert the list into its binary representation
        bin_u32list = u32list_to_bytes(_list)

        # get the start and end position of the block data 
        # (relative to the block data)
        end = block.end_data + len(bin_u32list)
        start = block.end_data

        # update the data in the block
        block.num_items += len(_list)
        block.end_data = end #+1?

        # allow direct access to the memory in the block data 
        # and write to the specified location in memory
        mem_datablock = memoryview(block.data)
        mem_datablock[start:end] = bin_u32list
        
        self.write(block_pos, block)

