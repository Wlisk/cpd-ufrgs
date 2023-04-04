# importing types
from io import BufferedReader
from scripts.types import EntityInfo, AllHType, AllEType

from struct import pack, unpack
from scripts.binaries.controls import ENTITY
from scripts.config import DATA_DIR

class IOBase:
    _file:          BufferedReader
    _filename:      str
    _entity:        EntityInfo
    _file_exists:   bool
    _header:        EntityInfo
    _headerdata:    AllHType
    _classtype:     AllEType

    def __init__(self, entity_name: str):
        self._entity = ENTITY[entity_name]
        self._filename = ''
        self._file = None
        self._file_exists = False
        self._header = None
        self._headerdata = None
        self._classtype = None

    # open the stream to read/write an entity file
    def open(self):
        if self._file == None:
            try:    
                self._file = open(self._filename, 'rb+')
                self._file_exists = True
            except: 
                self._file = open(self._filename, 'wb+')
                self._file_exists = False

    # close the stream of an entity file
    def close(self):
        if self._file != None: 
            self.write_header()
            self._file.close()
            self._file = None

    # write data at some position in the file
    def write_at(self, pos: int, data: bytes):
        self._file.seek(pos)
        self._file.write(data)

    # read n bytes from some pos in the file or read all data after pos
    def read_at(self, pos: int, size: int = 0) -> bytes:
        self._file.seek(pos)
        if size == 0: return self._file.read()
        return self._file.read(size)

    # read a header of an entity file
    def read_header(self) -> AllHType:
        self._file.seek(0)
        header_data = self._file.read(self._header.struct_size)
        # generate and return an object with the data read within
        return self._header.classtype.make( \
            unpack(self._header.struct_format, header_data) \
        )

    # update the header of the file with the new data
    # (overwrite all header section)
    def write_header(self):
        if self._headerdata == None: return
        bt_data = self._headerdata.to_bytestuple()
        # converts to a binary packed structure
        bin = pack(self._header.struct_format, *bt_data)
        self.write_at(0, bin)

    def read_all(self) -> list[AllEType]:
        return []