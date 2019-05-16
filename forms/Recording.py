from os import path
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QSpinBox, QRadioButton,
                             QTextEdit, QTableWidgetItem, QTableWidget, QAbstractItemView, QCheckBox, QComboBox)
from PyQt5.Qt import QIcon
from pynput.mouse import Controller
from pyscreeze import screenshot
from mouse import MouseControler
from datetime import datetime
from colorama import Fore
from database.database import get_sqlite3_db
from database.models import Script

tmouse = Controller()
basePath, filename = path.split(path.split(path.abspath(__file__))[0])


class Recording(QWidget):
    """
    主窗体
    """
    findcolor = None  # 找色区域
    configure = None  # 配置区域
    code = None  # 代码区域

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
        self.findcolor = FindColor()
        self.configure = Configure()
        self.code = Code()

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        glayout.addWidget(self.findcolor, 0, 0, 1, 1)
        glayout.addWidget(self.configure, 1, 0, 1, 1)
        glayout.addWidget(self.code, 2, 0, 1, 1)

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        self.code.signal.connect(self.slot)

    def slot(self, param):
        """
        槽函数
        :param param: Any
        :return:
        """
        func = getattr(self, param['function'], None)
        func(param)

    def reset_color_point(self, param=None):
        """
        重置所有找色点
        :return:
        """
        for i in range(1, 10):
            self.findcolor.clear(i)

    def generate_code(self, param=None):
        """
        生成代码
        :param param:
        :return:
        """
        if self.findcolor.ted_click_point.text() == '':
            QMessageBox.warning(None, '错误', '请添加【单击坐标】!', QMessageBox.Yes)
            return
        point_color_list = list()
        try:
            for key in [str(n) for n in range(1, 10)]:
                ted = getattr(self.findcolor, f'ted_color_{key}')
                if ted.text() != '':
                    point_color_dict = ted.text().split(': ')
                    point_color_dict = {
                        'point': eval(point_color_dict[0]),
                        'color': eval(point_color_dict[1].replace('rgb', ''))
                    }
                    point_color_list.append(point_color_dict)
            click_color_dict = self.findcolor.ted_click_point.text().split(': ')
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
        :param success_func: 成功回调函数 字符串 函数写在mouse.py中或import
        :param fail_func: 失败回调函数 字符串 函数写在mouse.py中或import
        """
        kwargs = {
            'retry_num': self.configure.spb_retry_num.value(),
            'retry_wait_time': self.configure.spb_retry_wait_time.value(),
            'pre_wait_time': self.configure.spb_pre_wait_time.value(),
            'button_type': self.configure.cmb_button_type.currentText(),
            'click_num': self.configure.spb_click_num.value(),
            'check_click_point_color': True if self.configure.ckb_click_point_color.isChecked() else False,
            'color_list': point_color_list
        }
        if self.configure.ted_success_func.text():
            kwargs['success_func'] = self.configure.ted_success_func.text()
        if self.configure.ted_fail_func.text():
            kwargs['fail_func'] = self.configure.ted_fail_func.text()
        cmd = f'MouseControler.clicks({click_color_dict}, **{kwargs})'
        self.code.ted_code.setText(cmd)
        self.code.ted_code.setStyleSheet('color: black')


class FindColor(QWidget):
    """
    找色区域
    """
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
            setattr(self, f'btn_clear_{i}', QPushButton('清空'))
        setattr(self, 'lab_click_point', QLabel('单击坐标:'))
        setattr(self, 'ted_click_point', QLineEdit())
        setattr(self, 'btn_clear_point', QPushButton('清空'))

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
            ted.setMinimumWidth(330)
            glayout.addWidget(ted, i - 1, 1, 1, 1)
            btn = getattr(self, f'btn_clear_{i}')
            glayout.addWidget(btn, i - 1, 2, 1, 1)
        glayout.addWidget(self.lab_click_point, i, 0, 1, 1)
        glayout.addWidget(self.ted_click_point, i, 1, 1, 1)
        glayout.addWidget(self.btn_clear_point, i, 2, 1, 1)
        self.setContentsMargins(-10, -10, -10, -10)  # 设置无边距

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        self.btn_clear_1.clicked.connect(lambda: self.clear(1))
        self.btn_clear_2.clicked.connect(lambda: self.clear(2))
        self.btn_clear_3.clicked.connect(lambda: self.clear(3))
        self.btn_clear_4.clicked.connect(lambda: self.clear(4))
        self.btn_clear_5.clicked.connect(lambda: self.clear(5))
        self.btn_clear_6.clicked.connect(lambda: self.clear(6))
        self.btn_clear_7.clicked.connect(lambda: self.clear(7))
        self.btn_clear_8.clicked.connect(lambda: self.clear(8))
        self.btn_clear_9.clicked.connect(lambda: self.clear(9))
        self.btn_clear_point.clicked.connect(lambda: self.clear('point'))

    def clear(self, i):
        """
        清空对应坐标和颜色
        :return:
        """
        if i == 'point':
            self.lab_click_point.setStyleSheet('')
            self.ted_click_point.setText('')
        else:
            lab = getattr(self, f'lab_color_{str(i)}')
            ted = getattr(self, f'ted_color_{str(i)}')
            lab.setStyleSheet('')
            ted.setText('')

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
            Static.get_color(lab, ted)
        elif key == "0":
            Static.get_color(self.lab_click_point, self.ted_click_point)


class Configure(QWidget):
    """
    配置区域
    """
    def __init__(self, parent=None):
        """
        初始化主窗体
        :param parent: 父级窗体
        """
        super(Configure, self).__init__(parent)
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
        setattr(self, 'ckb_click_point_color', QCheckBox('检测单击坐标色点'))  # 检测单击坐标色点多选框
        setattr(self, 'lab_pre_wait_time', QLabel('前置等待:'))  # 前置等待时间标签
        setattr(self, 'lab_retry_num', QLabel('重试次数:'))  # 重试次数标签
        setattr(self, 'lab_retry_wait_time', QLabel('重试等待:'))  # 重试等待时间标签
        setattr(self, 'lab_button_type', QLabel('按钮类型:'))  # 按钮类型标签
        setattr(self, 'lab_click_num', QLabel('单击次数:'))  # 单击次数标签
        setattr(self, 'spb_retry_num', QSpinBox())  # 重试次数计数条
        setattr(self, 'spb_retry_wait_time', QSpinBox())  # 重试等待时间计数条
        setattr(self, 'spb_pre_wait_time', QSpinBox())  # 前置等待时间计数条
        setattr(self, 'cmb_button_type', QComboBox())  # 按钮类型下拉框
        setattr(self, 'spb_click_num', QSpinBox())  # 单击次数计数条
        setattr(self, 'lab_success_func', QLabel('成功回调:'))  # 成功回调标签
        setattr(self, 'ted_success_func', QLineEdit())  # 成功回调编辑框
        setattr(self, 'lab_fail_func', QLabel('失败回调:'))  # 失败回调标签
        setattr(self, 'ted_fail_func', QLineEdit())  # 失败回调编辑框

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        glayout.addWidget(self.ckb_click_point_color, 0, 0, 1, 2)
        glayout.addWidget(self.lab_button_type, 0, 2, 1, 1)
        glayout.addWidget(self.cmb_button_type, 0, 3, 1, 1)
        widget_list = ['lab_pre_wait_time', 'spb_pre_wait_time', 'lab_click_num', 'spb_click_num',
                       'lab_retry_num', 'spb_retry_num', 'lab_retry_wait_time', 'spb_retry_wait_time',
                       'lab_success_func', 'ted_success_func', 'lab_fail_func', 'ted_fail_func']
        pos = [(r, c) for r in range(1, 4) for c in range(0, 4)]
        for position, name in zip(pos, widget_list):
            glayout.addWidget(getattr(self, name), *position)

        self.spb_pre_wait_time.setMaximum(60 * 1000)
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

        self.cmb_button_type.addItems(['左键', '右键', '不点击'])
        self.setContentsMargins(-10, -10, -10, -10)  # 设置无边距

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        pass


class Code(QWidget):
    """
    功能/代码区域
    """
    btn_reset = None  # 重置色点按钮
    btn_code = None  # 生成代码按钮
    btn_test = None  # 测试代码按钮
    btn_save = None  # 保存代码按钮
    ted_code = None  # 代码编辑框
    signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        """
        初始化主窗体
        :param parent: 父级窗体
        """
        super(Code, self).__init__(parent)
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
        self.btn_reset = QPushButton(QIcon(path.join(basePath, 'images/reset.ico')), '重置色点')  # 重置色点按钮
        self.btn_code = QPushButton(QIcon(path.join(basePath, 'images/code.ico')), '生成代码')  # 生成代码按钮
        self.btn_test = QPushButton(QIcon(path.join(basePath, 'images/test.ico')), '测试代码')  # 测试代码按钮
        self.btn_save = QPushButton(QIcon(path.join(basePath, 'images/save.ico')), '保存代码')  # 保存代码按钮
        self.ted_code = QTextEdit()  # 代码编辑框

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        widget_list = [self.btn_reset, self.btn_code, self.btn_test, self.btn_save]
        pos = [(r, c) for r in range(0, 1) for c in range(0, 4)]
        for position, widget in zip(pos, widget_list):
            glayout.addWidget(widget, *position)
        glayout.addWidget(self.ted_code, 1, 0, 1, 4)
        self.setContentsMargins(-10, -10, -10, -10)  # 设置无边距

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        self.btn_reset.clicked.connect(lambda: self.signal.emit({'function': 'reset_color_point'}))
        self.btn_code.clicked.connect(lambda: self.signal.emit({'function': 'generate_code'}))
        self.btn_test.clicked.connect(self.test_code)
        self.btn_save.clicked.connect(self.save_code)

    def save_code(self):
        """
        保存代码
        :return:
        """
        db = get_sqlite3_db()
        scripts = db.select_table(Script)
        max_sort = [i[1] for i in scripts]
        max_sort = int(max(max_sort)) if len(max_sort) > 0 else 0
        db.insert_table(Script, None, [[None, max_sort+1, self.ted_code.toPlainText(), '', True]])

    def test_code(self):
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


class Static:
    @staticmethod
    def set_data_source(db, class_, tablewidget, filter_dict=None):
        """
        设置TableView的数据源
        :param db: 数据源
        :param class_:sqla的类
        :param tablewidget: UI界面的tableview控件
        :param filter_dict: 过滤的字典
        :return:
        """
        tablewidget.setRowCount(0)  # 重置tablewidget
        # 获取header和数据
        header_list = db.get_model_columns(class_)
        tablewidget.setColumnCount(len(header_list))
        tablewidget.setHorizontalHeaderLabels(header_list)

        q_list = db.select_table(class_, filter_dict=filter_dict)
        # 将数据添加到tablewideget
        for r, rdata in enumerate(q_list):
            tablewidget.insertRow(r)
            for c, cell in enumerate(rdata):
                it = QTableWidgetItem(str(cell))
                tablewidget.setItem(r, c, it)

        # tableview.resizeColumnsToContents()  # 自动列宽
        tablewidget.horizontalHeader().setStretchLastSection(True)  # 充满tableview
        tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 单元格不可编辑
        # tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @staticmethod
    def main():
        from sys import argv, exit
        from PyQt5.Qt import QApplication
        app = QApplication(argv)
        main_form = Recording()
        # main_form = FindColor()
        main_form.show()
        exit(app.exec_())

    @staticmethod
    def get_color(lab, ted):
        """
        获取当前鼠标的像素RGB值
        :param lab:
        :param ted:
        :return:
        """
        x, y = tmouse.position
        # 由于截取的屏幕图像像素范围为鼠标坐标的2倍，这里需要四舍五入后获取转换后的坐标
        change_x = round(x * 2)
        change_y = round(y * 2)
        img = screenshot('my_screenshot.png')
        color = img.getpixel((change_x, change_y))[:3]
        img.close()
        rgb = f'rgb({color[0]}, {color[1]}, {color[2]})'
        lab.setStyleSheet(f"background-color: {rgb};")
        ted.setText(f'{str((x, y))}: {rgb}')


if __name__ == '__main__':
    Static.main()
