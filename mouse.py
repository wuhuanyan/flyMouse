from pynput.mouse import Button, Controller
from pynput import mouse
from datetime import datetime
from time import sleep
from pyscreeze import screenshot
from PIL import Image


tmouse = Controller()
script = './script1.txt'


class MouseListener:
    enable_move = False
    enable_scroll = True
    enable_click = True
    last_time = datetime.now()
    _script = script

    @classmethod
    def on_move(cls, x, y):
        if cls.enable_move:
            curr_time = datetime.now()
            point_location = (x, y)
            space_time = curr_time - cls.last_time
            space_time = space_time.seconds * 1000 + int(space_time.microseconds / 1000)
            with open(cls._script, 'a') as script_file:
                script_file.writelines(f'MouseControler.move({space_time}, {point_location})\n')
            cls.last_time = curr_time
        else:
            pass

    @classmethod
    def on_click(cls, x, y, button, pressed):
        if cls.enable_click:
            curr_time = datetime.now()
            point_location = (x, y)
            space_time = curr_time - cls.last_time
            space_time = space_time.seconds * 1000 + int(space_time.microseconds/1000)
            with open(cls._script, 'a') as script_file:
                script_file.write(f'MouseControler.control({space_time}, {point_location}, {pressed}, {button})\n')
            cls.last_time = curr_time
        else:
            pass

    @classmethod
    def on_scroll(cls, x, y, dx, dy):
        if cls.enable_scroll:
            curr_time = datetime.now()
            point_location = (x, y)
            space_time = curr_time - cls.last_time
            space_time = space_time.seconds * 1000 + int(space_time.microseconds / 1000)
            with open(cls._script, 'a') as script_file:
                script_file.writelines(f'MouseControler.scroll({space_time}, {point_location}, {dx}, {dy})\n')
            cls.last_time = curr_time
        else:
            pass

    @classmethod
    def start(cls):
        # 收集事件直到释放
        with mouse.Listener(on_move=cls.on_move, on_click=cls.on_click, on_scroll=cls.on_scroll) as listener:
            listener.join()


class MouseControler:

    @staticmethod
    def control(space_time, point_location, pressed, button):
        """
        执行鼠标单击或释放
        :param space_time: 执行前等待时间(毫秒)
        :param point_location: 鼠标坐标(x, y)
        :param pressed: 按下True/释放False
        :param button: Button.left/Button.right
        :return:
        """
        pressed_type = '按下' if pressed else '释放'
        button_type = '左键' if button == Button.left else '右键'
        print(f'[{space_time}]毫秒后, 在[{point_location}] [{pressed_type}] [{button_type}]')
        sleep(space_time/1000)
        tmouse.position = point_location
        sleep(50 / 1000)
        if pressed:
            tmouse.press(button)
        else:
            tmouse.release(button)

    @staticmethod
    def scroll(space_time, point_location, dx, dy):
        """
        滚动屏幕
        :param space_time: 执行前等待时间
        :param point_location: 鼠标坐标(x, y)
        :param dx: 负数: 向左滚动N步, 正数: 向右滚动N步 ?
        :param dy: 负数: 向下滚动N步, 正数: 向上滚动N步 ?
        :return:
        """
        print(f'[{space_time}]毫秒后, 在[{point_location}] 滚动({dx}, {dy})')
        sleep(space_time / 1000)
        tmouse.position = point_location
        sleep(50 / 1000)
        tmouse.scroll(dx, dy)

    @staticmethod
    def move(space_time, point_location):
        """
        移动鼠标
        :param space_time: 执行前等待时间
        :param point_location: 鼠标坐标(x, y)
        :return:
        """
        print(f'[{space_time}]毫秒后, 移动鼠标至:[{point_location}]')
        sleep(space_time / 1000)
        tmouse.position = point_location

    @staticmethod
    def clicks(click_point_dict, **kwargs):
        """
        :param click_point_dict: 单击点 {'point': (x, y), 'color': (r, g, b)}
        :param color_list: 颜色检测点 [{'point': (x, y), 'color': (r, g, b)}, ...]
        :param retry_num: 重试次数 int
        :param retry_wait_time: 重试等待时间 int(ms)
        :param pre_wait_time: 前置等待时间 int(ms)
        :param button_type: Button.left/Button.right
        :param click_num: 单击次数 int
        :param check_click_point_color: 是否校验单击坐标颜色 bool
        :return:
        """
        retry_num = kwargs.get('retry_num', 3)
        pre_wait_time = kwargs.get('pre_wait_time', 500)
        color_list = kwargs.get('color_list', [])
        retry_wait_time = kwargs.get('retry_wait_time', 500)
        check_click_point_color = kwargs.get('check_click_point_color', False)
        button_type = kwargs.get('button_type', 'left')
        click_num = kwargs.get('click_num', 1)
        button_type = Button.left if button_type == 'left' else Button.right

        if check_click_point_color:
            color_list.append(click_point_dict)

        sleep(pre_wait_time / 1000)
        for i in range(0, retry_num+1):
            check_status = MouseControler.check_color(color_list)
            if check_status:
                tmouse.position = click_point_dict['point']
                tmouse.click(button_type, click_num)
                return True
            else:
                print('屏幕颜色检测失败, 重试中!')
                sleep(retry_wait_time / 1000)
        return False

    @staticmethod
    def check_color(color_list):
        """
        检测当前屏幕是否符合颜色列表
        :param color_list: 颜色检测点 [{'point': (x, y), 'color': (r, g, b)}, ...]
        :return:
        """
        if len(color_list) == 0:
            return True
        else:
            screenshot('my_screenshot.png')
            img = Image.open('my_screenshot.png')
            for i in color_list:
                # 由于截取的屏幕图像像素范围为鼠标坐标的2倍，这里需要四舍五入后获取转换后的坐标
                x, y = i['point']
                change_x = round(x * 2)
                change_y = round(y * 2)
                if img.getpixel((change_x, change_y))[:3] != i['color']:
                    img.close()
                    return False
            img.close()
            return True


def main():
    # with open(script, 'w') as f:
    #     f.write('')
    # MouseListener.start()
    MouseControler.clicks({'point': (29.7578125, 11.4609375), 'color': (35, 47, 64)}, kargs={'retry_num': 1, 'retry_wait_time': 500, 'pre_wait_time': 500, 'button_type': 'left', 'click_num': 1, 'check_click_point_color': False})


if __name__ == '__main__':
    main()
