#!/bin/python3.7
import socket
import numpy as np
import mss
from threading import Thread
import threading

'''
Usage: python3.7 matrix_video_player_X6_independent_screens.py
'''

UDP_IP = '192.168.178.50'
UDP_PORT = [26113,26114,26116,26120,26128,26144]

offset_x = 100
offset_y = 10

input_size_x = 1024
input_size_y = 768

panel_offset_list = [[64, 0],
                    [64, 64],
                    [64, 128],
                    [64, 192],
                    [0, 64],
                    [128, 64]]

num_rows = 64
num_cols = num_rows
output_size_x = 256
output_size_y = 192
bin_size_x = int(input_size_x / output_size_x)
bin_size_y = int(input_size_y / output_size_y)
fbuf = np.zeros((num_rows), dtype='i4')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monitor = {'top': offset_y, 'left': offset_x, 'width': input_size_x, 'height': input_size_y}

def displayThread(_p, offx, offy, cast):
    for y in range(num_rows):
        for x in range(num_cols):
            addr = ((y & 0x3F) << 6) | (x & 0x3F);

            r = cast[y+offy][x+offx][2].item()
            g = cast[y+offy][x+offx][0].item()
            b = cast[y+offy][x+offx][1].item()

            fbuf[x] = socket.htonl((addr << 18)     | (((int(r))&0xFC) << 10)
                                                    | (((int(g))&0xFC) << 4)
                                                    | (((int(b))&0xFC) >> 2))
        s.sendto(fbuf.tobytes(), (UDP_IP, _p))

while(1):
    sct = mss.mss()
    cast = np.array(sct.grab(monitor), dtype='u4').reshape((output_size_x, bin_size_x, output_size_y, bin_size_y, 4)).max(3).max(1)
    sct.close()
    cast.astype(int)

    threads = []
    for i in range(6):
        t = Thread(target=displayThread, args=(UDP_PORT[i], panel_offset_list[i][0], panel_offset_list[i][1], cast)).start()


exit()
