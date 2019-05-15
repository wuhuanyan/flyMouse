from os import path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QSpinBox, QRadioButton,
                             QTextEdit)
from PyQt5.Qt import QImage, QIcon
from pynput.mouse import Controller
from pyscreeze import screenshot
from mouse import MouseControler
from datetime import datetime
from colorama import Fore
from database.database import get_sqlite3_db

tmouse = Controller()
basePath, filename = path.split(path.split(path.abspath(__file__))[0])


class Recording(QWidget):
    """
    主窗体
    """
    lab_color_1 = None  # 找色标签1
    lab_color_2 = None  # 找色标签2
    lab_color_3 = None  # 找色标签3
    lab_color_4 = None  # 找色标签4
    lab_color_5 = None  # 找色标签5
    lab_color_6 = None  # 找色标签6
    lab_color_7 = None  # 找色标签7
    lab_color_8 = None  # 找色标签8
    lab_color_9 = None  # 找色标签9
    lab_click = None  # 单击点标签

    ted_color_1 = None  # 找色编辑框1
    ted_color_2 = None  # 找色编辑框2
    ted_color_3 = None  # 找色编辑框3
    ted_color_4 = None  # 找色编辑框4
    ted_color_5 = None  # 找色编辑框5
    ted_color_6 = None  # 找色编辑框6
    ted_color_7 = None  # 找色编辑框7
    ted_color_8 = None  # 找色编辑框8
    ted_color_9 = None  # 找色编辑框9
    ted_click = None  # 单击点编辑框

    btn_clear_1 = None  # 清除坐标颜色按钮
    btn_clear_2 = None  # 清除坐标颜色按钮
    btn_clear_3 = None  # 清除坐标颜色按钮
    btn_clear_4 = None  # 清除坐标颜色按钮
    btn_clear_5 = None  # 清除坐标颜色按钮
    btn_clear_6 = None  # 清除坐标颜色按钮
    btn_clear_7 = None  # 清除坐标颜色按钮
    btn_clear_8 = None  # 清除坐标颜色按钮
    btn_clear_9 = None  # 清除坐标颜色按钮
    btn_click = None  # 清除坐标颜色按钮

    btn_reset = None  # 重置按钮
    btn_code = None  # 生成代码按钮
    btn_test = None  # 测试代码按钮
    btn_save = None  # 保存代码按钮

    lab_retry_num = None  # 重试次数标签
    lab_retry_wait_time = None  # 重试等待时间标签
    lab_pre_wait_time = None  # 前置等待时间标签
    lab_button_type = None  # 按钮类型标签
    lab_click_num = None  # 单击次数标签
    lab_check_point_color = None  # 单击坐标颜色

    spb_retry_num = None  # 重试次数计数条
    spb_retry_wait_time = None  # 重试等待时间计数条
    spb_pre_wait_time = None  # 前置等待时间计数条
    rdb_button_type_left = None  # 按钮类型单选框-左键
    rdb_button_type_right = None  # 按钮类型单选框-右键
    spb_click_num = None  # 单击次数计数条
    rdb_check_point_color = None  # 检查单击坐标颜色单选框
    rdb_ignore_point_color = None  # 忽略单击坐标颜色单选框

    ted_code = None  # 代码编辑框

    # keep_img = False  # 是否保留图像

    def __init__(self, parent=None):
        """
        初始化主窗体
        :param parent: 父级窗体
        """
        super(Recording, self).__init__(parent)
        self.init_subform()  # 初始化子窗体
        self.init_widget()  # 初始化窗体控件
        self.init_layout()  # 初始化控件布局
        self.init_btneven()  # 初始化按钮事件绑定
        self.parent = parent  # 父级窗体实例对象
        self.setWindowModality(Qt.ApplicationModal)  # 窗口置顶

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
        for i in range(1, 10):
            setattr(self, f'lab_color_{i}', QLabel(f'找色点{i}:'))
            setattr(self, f'ted_color_{i}', QLineEdit())
            setattr(self, f'btn_click_{i}', QPushButton('清空'))
        self.lab_click = QLabel('单击坐标:')
        self.ted_click = QLineEdit()
        self.btn_reset = QPushButton(QIcon(path.join(basePath, 'images/reset.ico')), '重置色点')
        self.btn_code = QPushButton(QIcon(path.join(basePath, 'images/code.ico')), '生成代码')
        self.btn_click = QPushButton('清空')  # 清除坐标颜色按钮

        self.lab_pre_wait_time = QLabel('前置等待:')  # 前置等待时间标签
        self.lab_retry_num = QLabel('重试次数:')  # 重试次数标签
        self.lab_retry_wait_time = QLabel('重试等待:')  # 重试等待时间标签
        self.lab_button_type = QLabel('按钮类型:')  # 按钮类型标签
        self.lab_click_num = QLabel('单击次数:')  # 单击次数标签
        self.lab_check_point_color = QLabel('单击颜色:')  # 单击坐标颜色

        self.spb_retry_num = QSpinBox()  # 重试次数计数条
        self.spb_retry_wait_time = QSpinBox()  # 重试等待时间计数条
        self.spb_pre_wait_time = QSpinBox()  # 前置等待时间计数条
        self.rdb_button_type_left = QRadioButton('左键')  # 按钮类型单选框-左键
        self.rdb_button_type_right = QRadioButton('右键')  # 按钮类型单选框-右键
        self.spb_click_num = QSpinBox()  # 单击次数计数条
        self.rdb_check_point_color = QRadioButton('检查')  # 检查单击坐标颜色单选框
        self.rdb_ignore_point_color = QRadioButton('忽略')  # 忽略单击坐标颜色单选框
        self.ted_code = QTextEdit()  # 代码编辑框
        self.btn_test = QPushButton(QIcon(path.join(basePath, 'images/test.ico')), '测试代码')  # 测试代码按钮
        self.btn_save = QPushButton(QIcon(path.join(basePath, 'images/save.ico')), '保存代码')  # 保存代码按钮

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        for i in range(1, 10):
            lab = getattr(self, f'lab_color_{i}')
            glayout.addWidget(lab, i - 1, 0, 1, 1)
            ted = getattr(self, f'ted_color_{i}')
            # ted.setEnabled(False)
            ted.setMinimumWidth(330)
            glayout.addWidget(ted, i - 1, 1, 1, 1)
            btn = getattr(self, f'btn_click_{i}')
            glayout.addWidget(btn, i - 1, 2, 1, 1)
        glayout.addWidget(self.lab_click, i, 0, 1, 1)
        glayout.addWidget(self.ted_click, i, 1, 1, 1)
        glayout.addWidget(self.btn_click, i, 2, 1, 1)

        widget = QWidget()
        widget.setContentsMargins(0, -10, 0, -10)  # 设置无边距
        wglayout = QGridLayout(widget)
        wglayout.addWidget(self.lab_check_point_color, 0, 0, 1, 1)
        widget1 = QWidget()
        widget1.setContentsMargins(-10, -10, -10, -10)  # 设置无边距
        wglayout1 = QGridLayout(widget1)
        wglayout1.addWidget(self.rdb_check_point_color, 0, 0, 1, 1)
        wglayout1.addWidget(self.rdb_ignore_point_color, 0, 1, 1, 1)
        wglayout.addWidget(widget1, 0, 1, 1, 2)
        wglayout.addWidget(self.lab_button_type, 0, 3, 1, 1)
        wglayout.addWidget(self.rdb_button_type_left, 0, 4, 1, 1)
        wglayout.addWidget(self.rdb_button_type_right, 0, 5, 1, 1)
        wglayout.addWidget(self.lab_pre_wait_time, 1, 0, 1, 1)
        wglayout.addWidget(self.spb_pre_wait_time, 1, 1, 1, 2)
        wglayout.addWidget(self.lab_click_num, 1, 3, 1, 1)
        wglayout.addWidget(self.spb_click_num, 1, 4, 1, 2)
        wglayout.addWidget(self.lab_retry_num, 2, 0, 1, 1)
        wglayout.addWidget(self.spb_retry_num, 2, 1, 1, 2)
        wglayout.addWidget(self.lab_retry_wait_time, 2, 3, 1, 1)
        wglayout.addWidget(self.spb_retry_wait_time, 2, 4, 1, 2)
        glayout.addWidget(widget, i + 1 + 0, 0, 1, 3)
        self.rdb_ignore_point_color.setChecked(True)
        self.rdb_button_type_left.setChecked(True)
        self.spb_pre_wait_time.setMaximum(60*1000)
        self.spb_pre_wait_time.setMinimum(10)
        self.spb_pre_wait_time.setValue(10)
        self.spb_retry_wait_time.setMaximum(60 * 1000)
        self.spb_retry_wait_time.setMinimum(10)
        self.spb_retry_wait_time.setValue(500)
        self.spb_click_num.setMaximum(9999)
        self.spb_click_num.setMinimum(1)
        self.spb_click_num.setValue(1)
        self.spb_retry_num.setMaximum(10)
        self.spb_retry_num.setMinimum(1)
        self.spb_retry_num.setValue(3)
        self.spb_pre_wait_time.setSuffix(' ms')
        self.spb_retry_num.setSuffix(' 次')
        self.spb_retry_wait_time.setSuffix(' ms')
        self.spb_click_num.setSuffix(' 次')
        widget = QWidget()
        wglayout = QGridLayout(widget)
        widget.setContentsMargins(0, -10, 0, -10)  # 设置无边距
        wglayout.addWidget(self.btn_reset, 0, 0, 1, 1)
        wglayout.addWidget(self.btn_code, 0, 1, 1, 1)
        wglayout.addWidget(self.btn_test, 0, 2, 1, 1)
        wglayout.addWidget(self.btn_save, 0, 3, 1, 1)
        glayout.addWidget(widget, i + 1 + 1, 0, 1, 3)
        glayout.addWidget(self.ted_code, i + 1 + 2, 0, 3, 3)

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        self.btn_reset.clicked.connect(self.reset)
        self.btn_code.clicked.connect(self.code)
        # for i in range(1, 10):
        #     btn = getattr(self, f'btn_click_{i}')
        #     btn.clicked.connect(lambda: self.clear(i))
        self.btn_click_1.clicked.connect(lambda: self.clear(1))
        self.btn_click_2.clicked.connect(lambda: self.clear(2))
        self.btn_click_3.clicked.connect(lambda: self.clear(3))
        self.btn_click_4.clicked.connect(lambda: self.clear(4))
        self.btn_click_5.clicked.connect(lambda: self.clear(5))
        self.btn_click_6.clicked.connect(lambda: self.clear(6))
        self.btn_click_7.clicked.connect(lambda: self.clear(7))
        self.btn_click_8.clicked.connect(lambda: self.clear(8))
        self.btn_click_9.clicked.connect(lambda: self.clear(9))
        self.btn_click.clicked.connect(lambda: self.clear('click'))
        self.btn_test.clicked.connect(self.test)
        self.btn_save.clicked.connect(self.save)

    def save(self):
        """
        保存代码
        :return:
        """
        db = get_sqlite3_db()
        db.test_connect()

    def test(self):
        """
        测试代码编辑框里的代码
        :return:
        """
        self.ted_code.setStyleSheet('color: black')
        cmd = self.ted_code.toPlainText()
        try:
            start_time = datetime.now()
            status = eval(cmd)
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()

            if status:
                self.ted_code.setStyleSheet('color: green')
                print(Fore.GREEN, '成功: 找色点击共计耗时:%s秒' % total_time, Fore.BLACK)
            else:
                self.ted_code.setStyleSheet('color: red')
                print(Fore.RED, '失败: 找色点击共计耗时:%s秒' % total_time, Fore.BLACK)
        except Exception as e:
            QMessageBox.warning(None, '错误', f'发生错误:\n{str(e)}', QMessageBox.Yes)

    def clear(self, i):
        """
        清空对应坐标和颜色
        :return:
        """
        if i == 'click':
            self.lab_click.setStyleSheet('')
            self.ted_click.setText('')
        else:
            lab = getattr(self, f'lab_color_{str(i)}')
            ted = getattr(self, f'ted_color_{str(i)}')
            lab.setStyleSheet('')
            ted.setText('')

    def reset(self):
        """
        重置信息
        :return:
        """
        # self.keep_img = False
        for i in range(1, 10):
            lab = getattr(self, f'lab_color_{i}')
            ted = getattr(self, f'ted_color_{i}')
            lab.setStyleSheet('')
            ted.setText('')
        # self.lab_click.setStyleSheet('')
        # self.ted_click.setText('')

    def code(self):
        """
        生成代码, 颜色检测并单击代码
        :return:
        """
        if self.ted_click.text() == '':
            QMessageBox.warning(None, '错误', '请添加【单击坐标】!', QMessageBox.Yes)
            return
        point_color_list = list()
        try:
            for key in [str(n) for n in range(1, 10)]:
                ted = getattr(self, f'ted_color_{key}')
                if ted.text() != '':
                    point_color_dict = ted.text().split(': ')
                    point_color_dict = {
                        'point': eval(point_color_dict[0]),
                        'color': eval(point_color_dict[1].replace('rgb', ''))
                    }
                    point_color_list.append(point_color_dict)
            click_color_dict = self.ted_click.text().split(': ')
            click_color_dict = {
                'point': eval(click_color_dict[0]),
                'color': eval(click_color_dict[1].replace('rgb', ''))
            }
        except Exception as e:
            QMessageBox.warning(None, '错误', f'发生错误:\n{str(e)}', QMessageBox.Yes)
            return

        """
        :param click_point_dict: 单击点 {'point': (x, y), 'color': (r, g, b)}
        :param color_list: 颜色检测点 [{'point': (x, y), 'color': (r, g, b)}, ...]
        :param retry_num: 重试次数 int
        :param retry_wait_time: 重试等待时间 int(ms)
        :param pre_wait_time: 前置等待时间 int(ms)
        :param button_type: Button.left/Button.right
        :param click_num: 单击次数 int
        :param check_click_point_color: 是否校验单击坐标颜色 bool
        """
        kwargs = {
            'retry_num': self.spb_retry_num.value(),
            'retry_wait_time': self.spb_retry_wait_time.value(),
            'pre_wait_time': self.spb_pre_wait_time.value(),
            'button_type': 'left' if self.rdb_button_type_left.isChecked() else 'right',
            'click_num': self.spb_click_num.value(),
            'check_click_point_color': True if self.rdb_check_point_color.isChecked() else False,
            'color_list': point_color_list
        }
        cmd = f'MouseControler.clicks({click_color_dict}, **{kwargs})'
        # print(cmd)
        self.ted_code.setText(cmd)
        self.ted_code.setStyleSheet('color: black')

    def keyReleaseEvent(self, key_event):
        """
        局部热键
        :param key_event:
        :return:
        """
        key_dict = {
            16777264: '1',
            16777265: '2',
            16777266: '3',
            16777267: '4',
            16777268: '5',
            16777269: '6',
            16777270: '7',
            16777271: '8',
            16777272: '9',
            16777273: '0'
        }
        key = key_dict.get(key_event.key(), None)

        if key in [str(n) for n in range(1, 10)]:
            lab = getattr(self, f'lab_color_{key}')
            ted = getattr(self, f'ted_color_{key}')
            self.get_color(lab, ted)
        elif key == "0":
            self.get_color(self.lab_click, self.ted_click)

    @staticmethod
    def get_color(lab, ted):
        """
        获取当前鼠标的像素RGB值
        :param lab:
        :param ted:
        :return:
        """
        x, y = tmouse.position
        # if self.keep_img:  # 如果有保留图像则直接读取
        #     pass
        # else:  # 否则截图
        #     screenshot('my_screenshot.png')
        screenshot('my_screenshot.png')
        img = QImage('my_screenshot.png')
        # 由于截取的屏幕图像像素范围为鼠标坐标的2倍，这里需要四舍五入后获取转换后的坐标
        change_x = round(x*2)
        change_y = round(y*2)
        color = img.pixelColor(change_x, change_y).getRgb()[:3]
        rgb = f'rgb({color[0]}, {color[1]}, {color[2]})'
        lab.setStyleSheet(f"background-color: {rgb};")
        ted.setText(f'{str((x, y))}: {rgb}')
        # self.keep_img = True
