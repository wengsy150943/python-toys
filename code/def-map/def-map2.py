import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读入数据
config = open('config.txt', 'r', encoding='utf8').readlines()

title = ''
dim = ['' for i in range(2)]
rg = ['' for i in range(3)]
describe = [['' for i in range(3)] for j in range(2)]
imgurl = [['' for i in range(3)] for j in range(3)]
dif = [['' for i in range(4)] for j in range(4)]

for i, v in enumerate(config):
    content = v.strip()
    if content == '标题':
        title = config[i + 1]
    elif content == '维度':
        dim = config[i + 1].strip().split()
    elif content == '分类':
        rg = config[i + 1].strip().split()
    elif content == '维度描述':
        for j, v in enumerate(config[i + 1].strip().split()):
            describe[0][j] = v
        for j, v in enumerate(config[i + 2].strip().split()):
            describe[1][j] = v
    elif content == '图片名':
        for j, v in enumerate(config[i + 1].strip().split()):
            imgurl[0][j] = v
        for j, v in enumerate(config[i + 2].strip().split()):
            imgurl[1][j] = v
        for j, v in enumerate(config[i + 3].strip().split()):
            imgurl[2][j] = v
    elif content == '图片描述':
        for j, v in enumerate(config[i + 1].strip().split()):
            dif[1][j + 1] = v
        for j, v in enumerate(config[i + 2].strip().split()):
            dif[2][j + 1] = v
        for j, v in enumerate(config[i + 3].strip().split()):
            dif[3][j + 1] = v

img = [[None for i in range(4)] for j in range(4)]

img[0][0] = title + '\n' + "九宫格"
for i in range(3):
    img[0][i+1] = dim[0]+rg[i]+'\n'+describe[0][i]
  
for i in range(3):
    img[i+1][0] = dim[1]+rg[i]+'\n'+describe[1][i]


# 绘制
plt.figure(figsize=(10,10))
grid = plt.GridSpec(7, 8)
for i in range(4):
    for j in range(4):
        if i==0:
            plt.subplot(grid[i*2:i*2+1,j*2:j*2+2])
        else:
            plt.subplot(grid[i*2-1:i*2+1,j*2:j*2+2])
            
        if img[i][j] is not None:
            plt.title(img[i][j],y=0.3,fontsize=15)
        else:
            plt.title(dif[i][j],y=-0.2,fontsize=10)
            plt.imshow(Image.open(imgurl[i-1][j-1]).resize((250,250)))
        plt.axis('off')
        

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=1)

#plt.savefig('def-map.png')
plt.show()