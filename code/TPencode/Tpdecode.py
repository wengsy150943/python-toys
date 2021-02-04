import numpy as np
#import os
from PIL import Image


def decode(ls):
    ls = [hex(i)[2:] for i in ls]
    ans = ''.join(ls)
    bs = bytes.fromhex(ans)
    fin = bs.decode()
    return fin

def de_image(ori_img, diff_img):
    ori = Image.open(ori_img)
    diff = Image.open(diff_img)
    ori_data = np.asarray(ori)
    diff_data = np.asarray(diff)
    ans = []
    col,row,channel = ori_data.shape
    for i in range(0,col):
        for j in range(0,row):
            for k in range(0,channel):
                temp = ori_data[i][j][k] ^ diff_data[i][j][k]
                if(temp == 0):return ans
                ans.append(temp - 1)
    return ans

ans = de_image("source.jpg", "target.png")
file = open("result.txt","w",encoding="utf8")
print(decode(ans),file=file)