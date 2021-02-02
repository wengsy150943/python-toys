import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

fig = plt.figure()

data = np.array(0)


def update(frame):
    # 清除画布，不然均值和标准差的线会糊成一团
    plt.cla()
    plt.ylim(0, 100)
    plt.xlim(-5, 5)
    # 不断追加生成的随机数
    global data
    data = np.append(data, np.random.randn(20))
    # 计算均值
    mean = np.mean(data)
    plt.axvline(x=mean, ls="-", label="mean")
    # 计算标准差，绘制3 sigma的范围
    std = np.std(data)
    plt.axvspan(xmin=mean - std,
                xmax=mean + std,
                facecolor='blue',
                alpha=0.2,
                label="1 $\sigma$")
    plt.axvspan(xmin=mean - 2 * std,
                xmax=mean + 2 * std,
                facecolor='blue',
                alpha=0.2,
                label="2 $\sigma$")
    plt.axvspan(xmin=mean - 3 * std,
                xmax=mean + 3 * std,
                facecolor='blue',
                alpha=0.1,
                label="3 $\sigma$")

    plt.legend()
    # 绘制图像
    hist = plt.hist(data, 60, density=False, facecolor="blue")
    return hist,


ani = FuncAnimation(fig, update, frames=100, interval=200)
ani.save("./test.gif", writer='pillow')
plt.show()