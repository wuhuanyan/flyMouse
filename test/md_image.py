import base64
f = open('../README/CFE1A181-69F1-489E-919A-A0BC00F9DD3B.png', 'rb')  # 二进制方式打开图文件
ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
f.close()
print(ls_f)
