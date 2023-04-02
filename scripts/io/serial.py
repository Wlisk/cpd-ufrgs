# importing types
from scripts.types import HeaderType, CollectionType
from scripts.io.iobase import IOBase

from struct import pack, unpack, iter_unpack
from scripts.binaries.controls import HEADER
from io import SEEK_END

# 
class Serial(IOBase):
    def __init__(self, entity_name: str):
        super().__init__(entity_name)
        self._header = HEADER
        self._headerdata = HeaderType(0, self._entity.struct_size)

    def open(self):
        super().open()
        if not self._file_exists:
            self._file_exists = True
            super().write_header()
        else:
            self._headerdata = super().read_header()

    # read all entity file and return a list of items
    def read_all(self) -> list[CollectionType]:
        # read all data starting from the header
        data = super().read_at(self._header.struct_size)
        # get item by item from the data read and create a list from all items
        return [\
            CollectionType.make(item).normalize() \
            for item in iter_unpack(self._entity.struct_format, data) \
        ]

    # write a list of items into an entity file
    # (overwrites all data starting from the head)
    def write_all(self, data: list[CollectionType]):
        # update header with the new num of items
        self._headerdata.num_items = len(data)
        # write each item into the entity file
        for item in data:
            bt_item = item.to_bytestuple()
            self._file.write(pack(self._entity.struct_format, *bt_item))
        super().write_header()

    # returns a generator for the data read
    # can pass a file position to start the reading
    def read(self, pos: int = 0):
        size = self._entity.struct_size
        pos = pos if pos > 0 else self._header.struct_size
        self._file.seek(pos)
        while item := self._file.read(size):
            # if end of file or cannot read offset bytes further then exit loop
            # as there is no more entity data to read
            if len(item) < size: break
            # return the item read
            yield  CollectionType.make(\
                unpack(self._entity.struct_format, item) \
            ).normalize()

    # write an item at the end of the entity file
    def write(self, data: CollectionType):
        self._file.seek(0, SEEK_END)
        self._headerdata.num_items += 1
        bt_data = data.to_bytestuple()
        self._file.write(pack(self._entity.struct_format, *bt_data))
