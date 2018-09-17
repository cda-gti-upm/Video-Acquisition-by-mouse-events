# -*- coding: utf-8 -*-

import Leap, struct, ctypes 

frames = []
with open("savedframes.data", "rb") as data_file:
    next_block_size = data_file.read(4)
    while next_block_size:
        size = struct.unpack('i', next_block_size)[0]
        data = data_file.read(size)
        leap_byte_array = Leap.byte_array(size)
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, data, size)
        print("Block read")

        frame = Leap.Frame()
        frame.deserialize((leap_byte_array, size))
        next_block_size = data_file.read(4)
        frames.append(frame)
        
        
for hand in frames[0].hands:
    for finger in hand.fingers:
        if finger.type == 1:
            print(str(finger.tip_position))