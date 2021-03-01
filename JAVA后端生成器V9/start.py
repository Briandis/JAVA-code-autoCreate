from src.httpServer.server import Server
import json
import _thread
import sys
import os

from src.servlet.linkMySql import *

if __name__ == '__main__':
    print("默认端口11451")
    port = 11451
    ip = ""
    print("开始将本启动器下的html设为web文件夹")
    path = os.path.join(os.getcwd(), "html")
    print(f"服务器静态资源路径:{path}")
    listen_size = 35
    run_flag = False
    while True:
        try:
            server_obj = Server(path, address=(ip, port), listen_size=listen_size)
            print(f"服务器地址：http://127.0.0.1:{port}")
            # 注册页面
            server_obj.index[""] = "/index.html"
            server_obj.index["/"] = "/index.html"
            server_obj.index["/index"] = "/index.html"
            server_obj.index["/index.html"] = "/index.html"
            # 注册servlet
            server_obj.servlet["/javaCode/login"] = LinkMySqlServlet()
            server_obj.servlet["/javaCode/createConfig"] = CreateConfigServlet()
            server_obj.servlet["/javaCode/create1"] = CreateOneServlet()
            server_obj.servlet["/javaCode/create2"] = CreateTowServlet()
            server_obj.servlet["/javaCode/create3"] = CreateThreeServlet()
            server_obj.servlet["/javaCode/getInfo"] = GetInfoServlet()
            server_obj.servlet["/javaCode/removeConfig"] = RemoveConfigServlet()
            server_obj.servlet["/javaCode/removeData"] = RemoveDataServlet()
            run_flag = True
            print("服务器启动成功")
            break
        except:
            string = input("端口被占用，输入数字更换端口，其他字符退出")
            if string.isnumeric():
                port = int(string)
    if run_flag:
        _thread.start_new_thread(server_obj.start, ())
        while server_obj.flag:
            flag = input("输入exit关闭服务器")
            if flag == "exit":
                server_obj.flag = False
        print("服务器开始关闭")
