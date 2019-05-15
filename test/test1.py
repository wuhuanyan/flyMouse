import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()

window.setWindowTitle("在屏幕中央显示窗口")

window.resize(300, 100)

window.move(window.width() * -2, 0)  # 先将窗口放到屏幕外，可避免移动窗口时的闪烁现象。

window.show()

desktop = QtWidgets.QApplication.desktop()

x = (desktop.width() - window.frameSize().width()) // 2

y = (desktop.height() - window.frameSize().height()) // 2

window.move(x, y)

sys.exit(app.exec_())