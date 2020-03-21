#!/bin/python3.7
import sys
from PIL import Image

'''
Usage: python3.7 image_to_splashscreen.py <path-to-image> <output-path>
'''

im = Image.open(sys.argv[1])
outpath = sys.argv[2]

needed_color_depth = 32;    #
alpha = 0                   # set to 1 if alpha is channel 0, to 0 if alpha is channel 3

mode = im.mode;
if mode != "RGBA" and mode != "RGB":
    print("Image mode not RGBA or RGB")
    exit()

actual_color_depth = 256;
cdiv = actual_color_depth/needed_color_depth;
pixels = list(im.getdata())

r = open(outpath+"red.mem","w+")
g = open(outpath+"green.mem","w+")
b = open(outpath+"blue.mem","w+")


for i in pixels:
    r.write('{:x}'.format((int)(i[1+alpha]/cdiv)) + '\n')
    g.write('{:x}'.format((int)(i[0+alpha]/cdiv)) + '\n')
    b.write('{:x}'.format((int)(i[2+alpha]/cdiv)) + '\n')

r.close()
g.close()
b.close()
