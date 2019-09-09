import zstandard as zstd
import sys
import io

def read8(f):
    return int.from_bytes(f.read(8), byteorder='little', signed=False)

def read4(f):
    return int.from_bytes(f.read(4), byteorder='little', signed=False)

def decomp_table(f, out_name):
    read4(f)
    read4(f)
    arc_size = read4(f)
    read4(f)

    i = f.read(arc_size)

    dctx = zstd.ZstdDecompressor()
    with open(out_name, "wb") as o:
        for chunk in dctx.read_to_iter(i):
            o.write(chunk)

class ArcHeader:
    MAGIC = 0xABCDEF9876543210
    def __init__(self, file):
        assert(read8(file) == self.MAGIC)
        self.StreamOffset = read8(file)
        self.FileDataOffset1 = read8(file)
        self.FileDataOffset2 = read8(file)
        self.FileSystemOffset1 = read8(file)
        self.FileSystemOffset2 = read8(file)
        read8(file) #padding

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] == "-h":
        print("Args format: [arc path] (minimum version 3.0.0)")
    else:
        with open(sys.argv[1], "rb") as arc:
            header = ArcHeader(arc)
            arc.seek(header.FileSystemOffset1)
            decomp_table(arc, "fs_table1.bin")
            arc.seek(header.FileSystemOffset2)
            decomp_table(arc, "fs_table2.bin")
