#! python3
# mouseNow.py - Displays the mouse cursor's current position.
import pyautogui
print('Press Ctrl-C to quit')
# TODO: Get and print the mouse coordinates.

try:
    while True:
        # TODO: Get and print the mouse coordinates.
        x,y = pyautogui.position()
        positionStr = 'X:'+ str(x).rjust(4) + '   Y:' + str(y).rjust(4)   #rjust() 字符串方法将对坐标右调整，让它们占据同样的宽度.
        pixelColor = pyautogui.screenshot().getpixel((x,y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr,end='')
        print('\b'*len(positionStr),end='',flush=True)
except KeyboardInterrupt:   # 当用户按下 Ctrl-C，程序执行将转到 except 子句
    print('\ndone')