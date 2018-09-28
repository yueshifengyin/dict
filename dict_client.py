'''
name: Lijia
data: 2018-10-1
email: it_lijialiang@163.com
modules:pymysql
This is a dict project for AID
'''

import sys
import getpass
from socket import *

# 创建网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(e)
        return
    # 连接成功后进入到一级界面
    while True:
        print('''
        ===========Welcome===========
        --- 1.注册  2.登录   3．退出---
        =============================
              ''')
        # 通过命令选项选择具体的功能
        cmd = input("请输入:")
        # 用户未注册时
        if cmd == '1':
            r = do_register(s)
            if r == 0:
                print("注册成功")
                # login(s, name) 直接进入二级界面
            elif r == 1:
                print("用户存在")
            else:
                print('注册失败')
        elif cmd == '2':
            name = do_login(s)
            if name:
                print("登录成功")
                login(s,name)
            else:
                print('用户名或密码不正确') 
        elif cmd == '3':
            s.send(b"E")
            print("退出客户端") 
            sys.exit(0)         

 
def do_register(s):
    while True:
        name = input("请输入用户名(q退出):")
        password = getpass.getpass()
        queren = getpass.getpass('请确认密码:')
        if (' ' in name) or (' ' in password):
            print("用户名不许有空格")
            continue
        if password != queren:
            print("两次密码不一致")
            continue
        if name == 'q':
            break

        msg = "R {} {}".format(name,password)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data = s.recv(128)

        if data == b'OK':
            return 0
        elif data == b"EXISTS":
            return 1
        else:
            return 2

def do_login(s):
    while True:
        name = input("请输入用户名:")
        password = getpass.getpass()
        msg = "L {} {}".format(name,password)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data = s.recv(128)
        if data == b'OK':
            return name
        else:
            return


def login(s, name):
    while True:
        print('''
        ===========查询界面===========
        --- 1.查词 2.历史记录 3．退出---
        =============================
               ''')
                # 通过命令选项选择具体的功能
        cmd = input("请输入:")

        if cmd == '1':
            do_query(s, name)
        elif cmd == '2':
            do_hist()
        elif cmd == '3':
            return


def do_query(s, name):
    while True:
        try:
            word = input('单词:')
        except KeyboardInterrupt:
            print("键盘退出")
            sys.exit(0)
        if word == '##':
            break
        msg = 'Q {} {}'.format(name,word)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("没有查到该单词")



def do_hist():
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("没有历史记录")


if __name__ == "__main__":
    main()
