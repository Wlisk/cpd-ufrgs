# type imports
from dataclasses import dataclass, astuple
from scripts.io.iobase import IOBase
from scripts.types import BlockHeaderType, BlockType

from io import SEEK_END
from scripts.config import BLOCK_SIZE, BLOCK_SIGNATURE
from struct import pack, unpack, iter_unpack
from scripts.binaries.controls import HEADER_BLOCK, BLOCK
from scripts.utils import get_filename
# 
class Blocks(IOBase):
    def __init__(self, entity_name: str):
        super().__init__(entity_name)
        self._header = HEADER_BLOCK
        self._headerdata = BlockHeaderType(0)
        self._filename = get_filename(self._entity.name, 'blocks')

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
        super().write_at(pos, pack(BLOCK.struct_format, *bt_block))
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
        super().write_at(\
            block_pos, \
            pack(self._header.struct_format, block.to_bytestuple()) \
        )

