import os
from PIL import Image,ImageFont,ImageDraw

config = open('config.txt','r',encoding='utf8').readlines()

title = ''
dim = ['' for i in range(2)]
rg = ['' for i in range(3)]
describe = [['' for i in range(3)] for j in range(2)]
imgurl = [['' for i in range(3)] for j in range(3)]
dif = [['' for i in range(4)] for j in range(4)]

for i,v in enumerate(config):
    content = v.strip()
    if content == '标题':
        title = config[i+1]
    elif content == '维度':
        dim = config[i+1].strip().split()
    elif content == '分类':
        rg = config[i+1].strip().split()
    elif content == '维度描述':
        for j,v in enumerate(config[i+1].strip().split()):
            describe[0][j] = v
        for j,v in enumerate(config[i+1].strip().split()): 
            describe[1][j] = v
    elif content == '图片名':
        for j,v in enumerate(config[i+1].strip().split()):
            imgurl[0][j] = v
        for j,v in enumerate(config[i+2].strip().split()):
            imgurl[1][j] = v
        for j,v in enumerate(config[i+3].strip().split()): 
            imgurl[2][j] = v
    elif content == '图片描述':
        for j,v in enumerate(config[i+1].strip().split()): 
            dif[1][j+1] = v
        for j,v in enumerate(config[i+2].strip().split()): 
            dif[2][j+1] = v
        for j,v in enumerate(config[i+3].strip().split()):
            dif[3][j+1] = v

img = [[None]*4,[None]*4,[None]*4,[None]*4]

img[0][0] = title.strip() + '\n' + "九宫格"
for i in range(3):
    img[0][i+1] = dim[0]+rg[i]+'\n'+describe[0][i]
  
for i in range(3):
    img[i+1][0] = dim[1]+rg[i]+'\n'+describe[1][i]

im = Image.new("RGB", (700, 700), (255, 255, 255))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 14)

dr.text((5,5),img[0][0],font=font, fill="#000000")
for i in range(3):
    dr.text((120+i*200,5),img[i+1][0],font=font, fill="#000000")
    dr.text((5,100+i*200),img[0][i+1],font=font, fill="#000000")
    dr.line([(110+i*200,0),(110+i*200,700)],fill=256)
    dr.line([(0,50+i*200),(700,50+i*200)],fill=256)

for i in range(3):
    for j in range(3):
        im.paste(Image.open(imgurl[i][j]).resize((128,128)),(120+i*200,100+j*200))
        dr.text((120+i*200,228+j*200),dif[i+1][j+1],font=font, fill="#000000")
im.save('def-map.png')