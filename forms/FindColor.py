from pynput.mouse import Controller
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QGridLayout, QWidget, QLabel)

tmouse = Controller()


class FindColor(QWidget):
    timer = None  # 定时器
    lab_x = None
    lab_y = None
    lab_color = None

    def __init__(self, parent=None):
        """
        初始化主窗体
        :param parent: 父级窗体
        """
        super(FindColor, self).__init__(parent)
        self.init_subform()  # 初始化子窗体
        self.init_widget()  # 初始化窗体控件
        self.init_layout()  # 初始化控件布局
        self.init_btneven()  # 初始化按钮事件绑定
        self.parent = parent  # 父级窗体实例对象
        # self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def init_subform(self):
        """
        初始化子窗体
        """
        pass

    def init_widget(self):
        """
        初始化窗体控件
        :return:
        """
        self.timer = QTimer()  # 初始化一个定时器
        self.lab_x = QLabel()
        self.lab_y = QLabel()
        self.lab_color = QLabel()

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        glayout.addWidget(self.lab_x, 0, 0, 1, 1)
        glayout.addWidget(self.lab_y, 1, 0, 1, 1)
        #  glayout.addWidget(self.lab_color, 2, 0, 1, 1)

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法

    def show(self):
        self.timer.start(20)  # 设置计时间隔并启动
        super(FindColor, self).show()

    def operate(self):
        x, y = tmouse.position
        self.lab_x.setText(f'X坐标:{x}')
        self.lab_y.setText(f'Y坐标:{y}')
        if y + self.height() + 30 >= 1050:
            change_y = y - self.height() - 30
        else:
            change_y = y + 10

        if x + self.width() + 10 >= 1680:
            change_x = x - self.width() - 10
        else:
            change_x = x + 10
        self.move(change_x, change_y)
