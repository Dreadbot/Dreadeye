import wpiutil
from wpiutil import wpistruct
import struct
class Position:
    def __init__(self, x: wpiutil.wpistruct.double, y: wpiutil.wpistruct.double, r: wpiutil.wpistruct.double, ID: wpiutil.wpistruct.int32):
        self.x = struct.pack('d', x)
        self.y = struct.pack('d', y)
        self.r = struct.pack('d', r)
        self.ID = ID

    def pack(self):
        bb = bytearray()
        self.packInto(bb)
        return bytes(bb)

    def packInto(self, bb: bytearray):
        bb.extend(self.x) #.tobytes())
        bb.extend(self.y) #.tobytes())
        bb.extend(self.r) #.tobytes())
        bb.extend(self.ID.to_bytes(4, byteorder='little'))

    def unpack(bb: bytearray):
        raise NotImplementedError("who called this?")

    WPIStruct = wpiutil.wpistruct.StructDescriptor(
        "struct:position",
        "double x;double y;double r;int ID",
        8 + 8 + 8 + 4,
        pack,
        packInto,
        unpack,
        None,
    )
