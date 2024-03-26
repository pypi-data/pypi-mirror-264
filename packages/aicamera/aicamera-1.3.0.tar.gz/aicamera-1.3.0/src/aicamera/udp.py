# -*- coding: utf-8 -*-
import socket
import time
import threading
import asyncio
import re
from . import cameraSocket
from . import rtsp
from . import util


# 服务器默认端口号
CLIENT_UDP_PORT = 44444
PY_UDP_PORT = 33333
sokectPort = util.getArg()

UDP_PORT = CLIENT_UDP_PORT if sokectPort is not None else PY_UDP_PORT

print(UDP_PORT)
if util.killByPort(UDP_PORT):
    print('sdk udp 被重新打开 历史打开的sdk udp 已经被关闭')
    time.sleep(1)


HQX_KEY = r'\$hqx-(.*)\$'
# HQX_KEY = '$hqx$'
# HQX_KEY = 'hello'

# 拉流地址
RTSP_URL = None

# 摄像头的信息
CAMERA_INFO = {
    "ip": None,
    "port": None,
}

CAMERA_ID  = None




'''
Date: 2024-02-18 13:57:43
author: zjs
description: udp  server
首次打开会有权限控制 需要教研和用户说
创建一个套接字socket对象，用于进行通讯

'''


def serverRun():
    print('开始接收udp广播')
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (util.getHostIp(),UDP_PORT)
    serverSocket.bind(address)
    # serverSocket.settimeout(10)  # 超时设置
    global RTSP_URL, CAMERA_INFO, CAMERA_ID
    while True:
        # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
        result, clientInfo = serverSocket.recvfrom(1024)
        result = result.decode("utf-8")
        print(f'ip:{clientInfo[0]},端口:{clientInfo[1]}，内容:{result}')  # 打印接收的内容
        match = re.search(HQX_KEY, result)
        # 过滤sin码
        sin = util.getArg('--sin') or 'SN000000000010'
        if sin and match.group(1) != sin:
            continue
        if match and not CAMERA_ID:
            CAMERA_ID = match.group(1)
            CAMERA_INFO['ip'] = clientInfo[0]
            CAMERA_INFO['port'] = clientInfo[1]
            RTSP_URL = f"rtsp://{clientInfo[0]}/live/main_stream"
            # 启动业务 sokect
            threading.Thread(target=lambda: asyncio.run(
                cameraSocket.runCameraSocket(clientInfo[0]))).start()
            # 等待业务 socket 启动
            while cameraSocket.cameraServiceSocket is None:
                time.sleep(0.8)
                pass
            # 是否启动socket api
            if sokectPort is not None:
                threading.Thread(target=lambda: asyncio.run(
                    cameraSocket.runSocketApi(sokectPort))).start()
                # 等待socket api 启动
                while cameraSocket.clientServiceSocket is None:
                    time.sleep(0.8)
                    pass
                print('启动 socket api')
            print('扫描到摄像头开始连接')
            # # 启动 rtsp 拉流
            threading.Thread(target=lambda: asyncio.run(
                rtsp.read(RTSP_URL))).start()
            # # 等待 rtsp 拉流
            while rtsp.ACTIVE_CAMERA is None:
                print('等待 rtsp 拉流')
                time.sleep(1)
                pass


'''
Date: 2024-02-18 14:10:38
author: zjs
description: client 发送端  目前协商是摄像头广播  该函数用于自己广播并接收测试
需要注意得是 如果严谨的话 先要扫描一些可以广播得ip 防止用户本地得网络配置不一样
然后多个广播地址同时广播
'''


def cilentRun():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # mock 地址
    sendIp = '192.168.1.255'
    mock = 1
    while True:
        serverAddress = (sendIp, UDP_PORT)
        clientSocket.sendto(str(HQX_KEY).encode('utf-8'), serverAddress)
        time.sleep(1)
        mock += 1
        if mock == 50:
            clientSocket.close()
            print('结束udp广播')
            return


'''
Date: 2024-02-22 15:20:52
author: zjs
description: 获取推流地址
'''


def getRtspUrl():
    return RTSP_URL
