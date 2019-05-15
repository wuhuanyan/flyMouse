import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QAction, QToolBar, QDesktopWidget, QRadioButton,
                             QCheckBox, QGridLayout, QWidget, QTabWidget)


class MainForm(QWidget):
    """
    主窗体
    """
    tab = None

    def __init__(self, parent=None):
        """
        初始化主窗体
        :param parent: 父级窗体
        """
        super(MainForm, self).__init__(parent)
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
        self.tab = QTabWidget()

    def init_layout(self):
        """
        初始化控件布局
        :return:
        """
        glayout = QGridLayout(self)
        glayout.addWidget(self.tab, 0, 0, 1, 1)

    def init_btneven(self):
        """
        初始化按钮事件绑定
        :return:
        """
        pass


def main():
    app = QApplication(sys.argv)
    dsManager = MainForm()
    dsManager.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()