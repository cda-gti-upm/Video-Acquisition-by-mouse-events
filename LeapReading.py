# -*- coding: utf-8 -*-

import Leap
import struct
import ctypes

frames = []
images = []

def main():
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    
    with open("savedframes.data", "rb") as data_file:
        next_block_size = data_file.read(4)
        while next_block_size:
            size = struct.unpack('i', next_block_size)[0]
            data = data_file.read(size)
            leap_byte_array = Leap.byte_array(size)
            address = leap_byte_array.cast().__long__()
            ctypes.memmove(address, data, size)
            
            frame = Leap.Frame()
            frame.deserialize((leap_byte_array, size))
            next_block_size = data_file.read(4)
            frames.append(frame)
            image = frame.images[0]
            
            """            
            for hand in frame.hands:
                for finger in hand.fingers:
                    if finger.type == 1:
                        print("Index position: " + str(finger.tip_position))"""
                                
if __name__ == "__main__":
    main()