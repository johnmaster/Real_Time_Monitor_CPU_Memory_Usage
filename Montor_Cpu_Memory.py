import matplotlib.pyplot as plt
import psutil
import time

plt.figure(facecolor='w')                      #修改画布背景颜色为白色

cpu_bar = plt.subplot(221)                     #cpu柱状图
cpu_line = plt.subplot(222)                    #cpu折线图
memory_bar = plt.subplot(223)                  #内存柱状图
memory_line = plt.subplot(224)                 #内存折线图

cpu_bar.set_position([0.125, 0.536, 0.1, 0.3])         #调整CPU柱状图在画布上的位置
cpu_line.set_position([0.3, 0.536, 0.6, 0.3])          #调整CPU折线图在画布上的位置
memory_bar.set_position([0.125, 0.1, 0.1, 0.3])        #调整内存柱状图在画布上的位置
memory_line.set_position([0.3, 0.1, 0.6, 0.3])         #调整内存折线图在画布上的位置

cpu_line.set_ylim(0, 100)                            #将2个图中Y轴的坐标范围定为0到100
memory_line.set_ylim(0, 100)

cpu_line.set_xlim(0, 20)                             #设置折线图X轴的坐标范围为0到20
memory_line.set_xlim(0, 20)

miloc_1 = plt.MultipleLocator(1)
miloc_2 = plt.MultipleLocator(10)
cpu_line.xaxis.set_minor_locator(miloc_1)
cpu_line.yaxis.set_minor_locator(miloc_2)
cpu_line.grid(which = 'minor', color = 'darkgray')                                      #折线图加方格线
memory_line.xaxis.set_minor_locator(miloc_1)
memory_line.yaxis.set_minor_locator(miloc_2)
memory_line.grid(which = 'minor')

cpu_bar.get_xaxis().set_visible(False)               #将CPU和内存的柱状图X坐标轴设为不可见
memory_bar.get_xaxis().set_visible(False)

x_2 = []                                           #存储CPU折线图的CPU使用率数据
y_2 = []
x_4 = []                                           #存储内存折线图使用率数据
y_4 = []

width = 1                                           #设置柱状图的宽度
step = 0                                            #折线图X轴的坐标
while True:                                         #开始绘图
    cpu_bar.cla()                                   #清除当前轴
    cpu_bar.set_ylim(0, 100)                        #设置CPU柱状图的Y轴范围为0到100
    temp_cpu = psutil.cpu_percent()                 #获取CPU利用率
    x_1 = [0]
    y_1 = [temp_cpu]
    cpu_bar.set_title(str(temp_cpu) + "%")                     #显示CPU利用率
    cpu_bar.bar(x_1, y_1, width=width)                         #绘制柱状图

    x_2.append(step)                                           #绘制折线图
    y_2.append(temp_cpu)
    if step > 20:                                              #折线图坐标轴移动
        cpu_line.set_xlim(step - 20, step)
        memory_line.set_xlim(step - 20, step)
    cpu_line.plot(x_2, y_2, color = 'b')

    #画内存的柱状图
    memory_bar.cla()
    memory_bar.set_ylim(0, 100)
    temp_memory = psutil.virtual_memory().percent               #获取内存使用率
    x_3 = [0]
    y_3 = [temp_memory]
    memory_bar.set_title(str(temp_memory) + '%')
    memory_bar.bar(x_3, y_3, width = width, color = 'r')

    x_4.append(step)
    y_4.append(temp_memory)
    memory_line.plot(x_4, y_4, color = 'r')
    step += 1
    plt.pause(0.5)

plt.show()