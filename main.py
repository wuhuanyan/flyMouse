import sys
import argparse
# from forms.MainForm import MainForm
# from forms.FindColor import FindColor
from forms.Recording import Recording
from PyQt5.QtWidgets import (QApplication)


parse = argparse.ArgumentParser(description="桌面按键精灵")
parse.add_argument("-m", "--main", action="store_true", help="使用GUI打开程序")
parse.add_argument("-r", "--run", nargs=1, metavar='scriptfile', help="运行脚本文件")
args = parse.parse_args()


def main():
    if args.main:
        Main().start()
    elif args.run is not None:
        print(args.run)
    else:
        Main().start()


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # self.main_form = MainForm()
        # self.main_form = FindColor()
        self.main_form = Recording()

    def start(self):
        """
        启动程序
        :return:
        """
        self.main_form.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    main()
