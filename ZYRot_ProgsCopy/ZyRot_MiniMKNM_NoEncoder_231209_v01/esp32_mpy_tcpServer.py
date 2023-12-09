"""
ESP32 TCP Server
"""

import socket
import network
from wifi_connect import do_connect

SSID = "HogPC"
PWD = "43215678"

port = 10000  #端口号
listenSocket = None  #套接字

try:
    # 注意：线连接到WiFi网络！
    # 如果未连接到网络，以下是连接到网络的代码
    #do_connect()
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
    ip = wlan.ifconfig()[0]   #获取IP地址
    print("ip:", ip)
    
    listenSocket = socket.socket()   #创建套接字
    listenSocket.bind((ip, port))   #绑定地址和端口号
    listenSocket.listen(1)   #监听套接字, 最多允许一个连接
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    print ('tcp waiting...')

    while True:
        print("accepting.....")
        conn, addr = listenSocket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
        print(addr, "connected")

        while True:
            data = conn.recv(1024)   #接收数据（1024字节大小）
            if(len(data) == 0):      #判断客户端是否断开连接
                print("close socket")
                conn.close()   #关闭套接字
                break
            #print("len:", len(data), "  ", data)
            print("len:", len(data))
            #ret = conn.send(data)   #发送数据
except:
    if(listenSocket):   #判断套接字是否为空
        listenSocket.close()   #关闭套接字
        
        