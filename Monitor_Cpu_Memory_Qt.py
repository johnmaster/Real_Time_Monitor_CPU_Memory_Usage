import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QColorDialog, QInputDialog
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtCore import QTimer
import psutil

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 600
        self.top = 300
        self.title = '实时监控CPU和内存利用率'
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('C:\\Users\\ThinkPad\\Desktop\\高级软件开发作业\\renwuguanliqi.png'))

        m = PlotCanvas(self, width=8, height=6)  # 实例化一个画布对象
        m.move(0, 0)
        # 设置选择图表颜色按钮
        color_button_graph = QPushButton('选择图表颜色', self)
        color_button_graph.move(200, 0)
        color_button_graph.clicked.connect(m.color_graph_draw)
        # 设置显示CPU按钮
        button_1 = QPushButton('显示CPU按钮', self)
        # button_1.setToolTip('This s an example button')
        button_1.move(100, 0)
        button_1.clicked.connect(m.plot_cpu)
        # 设置显示内存按钮
        button_2 = QPushButton('显示内存按钮', self)
        button_2.clicked.connect(m.plot_memory)
        # 设置选择网格颜色按钮
        color_button_grid = QPushButton('选择网格颜色', self)
        color_button_grid.move(300, 0)
        color_button_grid.clicked.connect(m.color_gird_draw)
        # 设置修改X轴网格密度
        x_grid_density = QPushButton('设置X轴网格密度', self)
        x_grid_density.move(400, 0)
        x_grid_density.clicked.connect(m.update_x_grid_density)
        # 设置修改Y轴网格密度
        y_grid_density = QPushButton('设置Y轴网格密度', self)
        y_grid_density.move(500, 0)
        y_grid_density.clicked.connect(m.update_y_grid_density)

        self.show()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='w')
        self.bar_graph = fig.add_subplot(121)                       # 左图是柱状图
        self.bar_graph.set_position([0.1, 0.0999, 0.1, 0.5])        # 调整柱状图的形状
        self.bar_graph.get_xaxis().set_visible(False)               # 设置柱状图X轴不可见

        self.line_graph = fig.add_subplot(122)                      # 右图是折线图
        self.line_graph.set_position([0.3, 0.0999, 0.65, 0.8])      # 调整折线图的形状

        self.line_graph.set_xlim(0, 20)
        self.line_graph.set_ylim(0, 100)

        self.bar_graph.set_ylim(0, 100)


        # CPU
        self.cpu_list = []
        self.cpu_x = []
        self.cpu_step = 0
        # 内存
        self.memory_list = []
        self.memory_x = []
        self.memory_step = 0
        # 设置图线默认颜色为蓝色
        self.graph_color = 'b'
        # 设置网格默认颜色
        self.grid_color = 'r'
        # 设置X轴默认网格密度
        self.x_density = 1
        # 设置Y轴默认网格密度
        self.y_density = 10

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def color_graph_draw(self):
        temp = QColorDialog.getColor()
        if temp.isValid():
            self.graph_color = temp.name()
        print("图表的颜色： ", self.graph_color)

    def color_gird_draw(self):
        temp = QColorDialog.getColor()
        if temp.isValid():
            self.grid_color = temp.name()
        print("网格的颜色： ", self.grid_color)

    def update_x_grid_density(self):
        num, density = QInputDialog.getDouble(self, '输入X轴网格密度', '输入数字')
        if density:
            self.x_density = num
        print("X轴网格密度：", num)

    def update_y_grid_density(self):
        num, density = QInputDialog.getDouble(self, '输入Y轴网格密度', '输入数字')
        if density:
            self.y_density = num
        print("Y轴网格密度：", num)

    def plot_cpu(self):
        try:
            self.memory_timer.stop()
        except Exception as e:
            print("关闭内存定时器出现  ", e, "  错误")
        try:
            self.cpu_timer.stop()
        except Exception as e:
            print("关闭CPU定时器出现  ", e, "  错误")
        self.line_graph.clear()
        self.line_graph.set_xlim(0, 20)
        self.line_graph.set_ylim(0, 100)
        self.cpu_list = []
        self.cpu_x = []
        self.cpu_step = 0
        # 设置CPU定时器
        self.cpu_timer = QTimer(self)
        self.cpu_timer.timeout.connect(self.update_cpu)
        self.cpu_timer.start(1000)

    def plot_memory(self):
        try:
            self.cpu_timer.stop()
        except Exception as e:
            print("关闭CPU定时器出现  ", e, "  错误")
        try:
            self.memory_timer.stop()
        except Exception as e:
            print("关闭内存定时器出现  ", e, "  错误")
        self.line_graph.clear()
        self.line_graph.set_xlim(0, 20)
        self.line_graph.set_ylim(0, 100)
        self.memory_list = []
        self.memory_x = []
        self.memory_step = 0
        # 设置内存定时器
        self.memory_timer = QTimer(self)
        self.memory_timer.timeout.connect(self.update_memory)
        self.memory_timer.start(1000)

    def update_cpu(self):
        # CPU柱状图
        cpu = psutil.cpu_percent()
        # 存储CPU使用率数据
        with open('C:\\Users\\ThinkPad\\Desktop\\cpu.txt', 'a+', encoding='utf-8') as f:
            temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  " + str(cpu) + "%" + '\n'
            f.write(temp)
            f.close()
        width = 1  # 柱状图宽度
        self.bar_graph.cla()
        self.bar_graph.set_ylim(0, 100)
        x_1 = [0]
        y_1 = [cpu]
        self.bar_graph.set_title("CPU: " + str(cpu) + "%")
        #设置网格线
        miloc_x = plt.MultipleLocator(self.x_density)
        miloc_y = plt.MultipleLocator(self.y_density)
        self.line_graph.xaxis.set_minor_locator(miloc_x)
        self.line_graph.yaxis.set_minor_locator(miloc_y)
        self.line_graph.grid(which='minor', color=self.grid_color, linestyle = '-')
        self.bar_graph.bar(x_1, y_1, width=width, color=self.graph_color)
        # CPU折线图
        self.cpu_x.append(self.cpu_step)
        self.cpu_list.append(cpu)
        if self.cpu_step > 20:
            self.line_graph.set_xlim(self.cpu_step - 20, self.cpu_step)
        self.line_graph.plot(self.cpu_x, self.cpu_list, color=self.graph_color)
        self.cpu_step += 1
        self.draw()

    def update_memory(self):
        # 内存柱状图
        memory = psutil.virtual_memory().percent
        with open('C:\\Users\\ThinkPad\\Desktop\\memory.txt', 'a+', encoding='utf-8') as f:
            temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  " + str(memory) + "%" + '\n'
            f.write(temp)
            f.close()
        width = 1  # 柱状图宽度
        self.bar_graph.cla()
        self.bar_graph.set_ylim(0, 100)
        x_1 = [0]
        y_1 = [memory]
        self.bar_graph.set_title("Memory: " + str(memory) + "%")
        #设置网格线
        miloc_x = plt.MultipleLocator(self.x_density)
        miloc_y = plt.MultipleLocator(self.y_density)
        self.line_graph.xaxis.set_minor_locator(miloc_x)
        self.line_graph.yaxis.set_minor_locator(miloc_y)
        self.line_graph.grid(which='minor', color=self.grid_color, linestyle = '-')
        self.bar_graph.bar(x_1, y_1, width=width, color=self.graph_color)
        # 内存折线图
        self.memory_x.append(self.memory_step)
        self.memory_list.append(memory)
        if self.memory_step > 20:
            self.line_graph.set_xlim(self.memory_step - 20, self.memory_step)
        self.line_graph.plot(self.memory_x, self.memory_list, color=self.graph_color)
        self.memory_step += 1
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

