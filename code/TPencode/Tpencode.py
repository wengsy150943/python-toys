import numpy as np
import os
from PIL import Image

def encode(filename):
    with open(filename,encoding="utf-8") as doc:
        file = doc.readlines()
        text = ''.join(file)
        byte = text.encode()
        hs = ''.join(['%02X' %x  for x in byte])
        ls = list(hs)
        ls = [int(i, 16) for i in ls]
    return ls



def en_image(imgname,ls):
    im = Image.open(imgname)
    data = np.array(im)
    l = len(ls)
    num = 0
    col,row,channel = data.shape
    for i in range(0,col):
        for j in range(0,row):
            for k in range(0,channel):
                data[i][j][k] = data[i][j][k] ^ (ls[num] + 1)
                num = num + 1
                if(l==num):return data

    return data


ls = encode("introduction.txt")
data = en_image("source.jpg", ls)
new_im = Image.fromarray(data)
new_im.save("target.png")

