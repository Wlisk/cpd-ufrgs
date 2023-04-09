# type imports
from io             import BufferedReader
from scripts.types  import EntityInfo, AllHType, AllEType
# module imports 
from struct         import pack, unpack
# const imports
from scripts.binaries.controls import ENTITY

class IOBase:
    _file:          BufferedReader      # file stream
    _filename:      str                 # path and filename with extension
    _entity:        EntityInfo          # info about an entity file
    _file_exists:   bool                # if the file was created
    _header:        EntityInfo          # header info for entity/block file
    _headerdata:    AllHType            # the data of the header
    _classtype:     AllEType            # utility to create class instances

    # initialize with default 'null' values
    def __init__(self, entity_name: str):
        self._entity = ENTITY[entity_name]
        self._filename = ''
        self._file = None
        self._header = None
        self._headerdata = None
        self._classtype = None

    # open the stream to read/write an entity/block file
    def open(self):
        if self._file == None:
            # if the file exists, open in read and write b-mode
            try:    
                self._file = open(self._filename, 'rb+')
                self._headerdata = self.read_header()
            # otherwise create the file and open in write and read b-mode
            except: 
                self._file = open(self._filename, 'wb+')
                # notice that if the file does not exists, after creating it
                # its total size would be 0, so to not cause errors 
                # we write its header right after creating it
                self.write_header()

    # close the stream of an entity/block file
    def close(self):
        if self._file != None: 
            self.write_header() # update the header before closing
            self._file.close()
            self._file = None

    # write data at some position in the file
    def write_at(self, pos: int, data: bytes|bytearray):
        self._file.seek(pos)
        self._file.write(data)

    # read n bytes from some pos in the file or read all data after pos
    def read_at(self, pos: int, size: int = 0) -> bytes:
        self._file.seek(pos)
        if size == 0: return self._file.read()
        return self._file.read(size)

    # read a header of an entity file
    def read_header(self) -> AllHType:
        header_bin = self.read_at(0, self._header.struct_size)
        # generate and return an object with the data read within
        return self._header.classtype.make( \
            unpack(self._header.struct_format, header_bin) \
        )

    # update the header of the file with the new data
    # (overwrite all header section)
    def write_header(self):
        if self._headerdata == None: return
        bt_data = self._headerdata.to_bytestuple()
        # converts to a binary packed structure and write into the file
        self.write_at(0, pack(self._header.struct_format, *bt_data))
