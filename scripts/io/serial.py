# type imports
from typing             import Generator
from scripts.types      import HeaderType, AllEType
from scripts.io.iobase  import IOBase
# module imports
from struct             import pack, iter_unpack, unpack
from scripts.utils      import get_filename
# const imports
from io                 import SEEK_END
from scripts.io.controls import HEADER

# tools for read/write entity files
class Serial(IOBase):
    _headerdata: HeaderType     # the data of the header
    
    # receives the name and the class of the entity file
    def __init__(self, entity_name: str, classtype: AllEType):
        super().__init__(entity_name)
        self._header        = HEADER
        self._headerdata    = HeaderType(0, self._entity.struct_size)
        self._classtype     = classtype
        self._filename      = get_filename(entity_name, 'serial')

    # read all entity file and return a list of items
    def read_all(self) -> list[AllEType]:
        # read all data starting from the header
        data = super().read_at(self._header.struct_size)
        # get item by item from the data read 
        # and create a list with them
        if len(data) == 0: return []
        return [\
            self._classtype.make(item).normalize() \
            for item in iter_unpack(self._entity.struct_format, data) \
        ]

    # write an item at the end of the entity file
    # and return its position
    def write(self, data: AllEType) -> int:
        #set the position to the end of the file
        pos = self._file.seek(0, SEEK_END)
        # update the header
        self._headerdata.num_items += 1
        # convert data to tuple so we can easily pack it into binary
        # and then write it into the entity file
        bt_data = data.to_bytestuple()
        self._file.write(pack(self._entity.struct_format, *bt_data))
        # return the pos where the item was written
        return pos
    
    # returns a generator for the data read
    # start reading after the header pos (0) or the given pos
    def read(self, pos: int = 0) -> Generator[AllEType, None, None]:
        # save the size of the item structure
        size = self._entity.struct_size
        # computes the offset/position of the file to start reading
        pos = pos if pos > 0 else self._header.struct_size
        self._file.seek(pos)
        # while there is items to read
        while item := self._file.read(size):
            # if end of file or cannot read offset bytes further 
            # then exit from the loop
            # as there is no more entity data to read
            if len(item) < size: break
            # return the item read
            yield self._classtype.make(\
                unpack(self._entity.struct_format, item) \
            ).normalize()

    # reads an item at the given position
    def read_item(self, pos: int) -> AllEType:
        # save the size of the item structure
        size = self._entity.struct_size
        # computes the offset/position of the file to start reading
        pos = pos if pos > 0 else self._header.struct_size
        self._file.seek(pos)
        item = self._file.read(size)
        # if no items to read (based on the read len)
        if len(item) < size: return None
        # return the item read
        return self._classtype.make(\
            unpack(self._entity.struct_format, item) \
        ).normalize()
