'''
Date: 2024-02-18 15:37:29
author: zjs
'''
import asyncio
import websockets
import socket
import json
import inspect
import struct
import time
from . import util
from . import udp
# 摄像头业务 socket 端口号
CAMERA_WS_PORT = 55555

# 摄像头业务socket
cameraServiceSocket = None

# 客户端业务socket
clientServiceSocket = None

# 摄像头服务端是否连接
isServerConnect = False
# 摄像头客户端是否连接
isClientConnect = False

# socket 返回值 根据uuid
socketResult = {}

# 改成两个客户端 通讯代理
'''
Date: 2024-02-18 15:46:25
author: zjs
description:获取摄像头业务 sokect
'''


async def runCameraSocket(cameraIp):
    if cameraIp is None:
        print('摄像头ip不存在 runCameraSocket')
        return
    global cameraServiceSocket, clientServiceSocket,isServerConnect
    if isServerConnect:
        print('摄像头服务端socket正在连接中')
        return
    try:
        cameraServiceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cameraServiceSocket.connect((cameraIp, CAMERA_WS_PORT))
        isServerConnect = True
        print('摄像头连接成功')
        while True:
            serverMsg = cameraServiceSocket.recv(1024)
            print(serverMsg, '摄像头 ===>>>   py   ===>>>  客户端',[serverMsg[-4],serverMsg[-3]])
            if len(serverMsg) > 4 and serverMsg[0] == 0x7e and serverMsg[1] == 0x7e:
                uuidNum = serverMsg[-4] | serverMsg[-3] << 8
                socketResult[uuidNum] = serverMsg
            if clientServiceSocket :
                await clientServiceSocket.send(serverMsg)
            await asyncio.sleep(0.05)
    except Exception as e:
        isServerConnect=False
        cameraServiceSocket.close()
        udp.CAMERA_INFO=None
        print('gewu sokect 读写错误1', e)


'''
Date: 2024-02-19 17:43:27
author: zjs
description:  启动 socket 接口(http) 服务
'''


async def runSocketApi(sokectPort):
    global cameraServiceSocket, clientServiceSocket,isClientConnect
    if isClientConnect:
        print('摄像头客户端socket正在连接中')
        return
    async with websockets.connect(f'ws://127.0.0.1:{sokectPort}') as cilentWs:
        clientServiceSocket = cilentWs
        try:
            await __sendRtspUrlByClient()
            isClientConnect = True
            while True:
                # # 50ms接收数据
                clientMsg = await cilentWs.recv()
                if not clientMsg or clientMsg == 'jump':
                    continue
                # key value
                jsonResult = json.loads(clientMsg)
                print(jsonResult, '客户端 ===>>> py  ===>>>   摄像头')
                key = jsonResult['key']
                value=None
                uuid=None
                if 'value' in jsonResult:
                    value =jsonResult['value']
                if 'uuid' in jsonResult:
                    uuid =jsonResult['uuid']
                config = {
                    'useMode': lambda val,uuid: async_use_mode(val,uuid),
                    'reTrain': lambda val,uuid: __reTrain(val,uuid),
                    'getRes': lambda val,uuid: async_get_res(uuid),
                }
                activeMethod = config[key]
                if activeMethod:
                    activeMethod(value,uuid)
                await asyncio.sleep(0.05)
        except Exception as e:
            udp.CAMERA_INFO=None
            isClientConnect = False
            print('gewu sokect 读写错误2', e)

# 模型cmd
modeType = {
    'face_detect': 0x01,  # 人脸检测
    'traffic_sign': 0x02,  # 交通标志
    'qr_code': 0x03,  # 二维码
    'bar_code': 0x04,  # 条形码
    'face_recognition': 0x05,  # 人脸识别
    'classify': 0x06,  # 分类
    'gesture': 0x07,  # 手势
    'car_number': 0x08,  # 车牌
    'trace': 0x09,  # 物体追踪
}

'''
Date: 2024-02-22 11:58:38
author: zjs
description: 等待指定uuid 消息返回结果
'''

def waitSocketResult (uuid,cb =None):
    socketResult[uuid] = None
    startTime = time.time()
    speedTime = time.time()
    result = []
    # 等待结果
    while socketResult[uuid] is None and (time.time() - startTime) < 30:
        time.sleep(0.1)
        if (time.time() - speedTime) > 3:
            speedTime = time.time()
            print('与摄像头通讯中')
        pass

    if ((time.time() - startTime) > 30) or not socketResult[uuid]:
        print('=== 摄像头通讯超时 ===')
        return result

    activeSocketResult = socketResult[uuid]
    if activeSocketResult[4] != 0x01 or activeSocketResult[3] != 0x04:
        print('摄像头通讯失败')
    if inspect.isfunction(cb):
        result = cb(activeSocketResult)

    if uuid in socketResult:
        del socketResult[uuid]

    return result



'''
Date: 2024-02-22 11:58:38
author: zjs
description: 设置算法使用
'''

def use_mode(mode,uuidHex=util.genUuid()):
    if not any(el == mode for el in list(modeType.keys())):
        return print(f'没有 {mode} 模式')
    cmd = 0x01
    cameraServiceSocket.sendall(util.genSendPack(cmd=cmd, subcmd=modeType[mode],uuid=uuidHex))
    waitSocketResult(uuid = (uuidHex[0]|(uuidHex[1]<<8)))

'''
Date: 2024-02-22 11:58:38
author: zjs
description: 设置算法使用 异步版本给js 用
'''
def async_use_mode(mode,uuid):
    if not any(el == mode for el in list(modeType.keys())):
        return print(f'没有 {mode} 模式')
    cmd = 0x01
    cameraServiceSocket.sendall(util.genSendPack(cmd=cmd, subcmd=modeType[mode],uuid=uuid))



'''
Date: 2024-02-22 11:58:38
author: zjs
description: 重新训练模型
'''


def __reTrain(val,uuid):
    mode, url = val['mode'], val['url']
    if not any(el == mode for el in [
       'classify',
       'face_detect'
    ]):
        return print(f'没有 {mode} 模式')
    cmd = 0x02
    cameraServiceSocket.sendall(
        util.genSendPack(cmd=cmd, subcmd=modeType[mode],data=url,uuid=uuid))



resultType = {
    'result': 0x00,  # 结果
    '其他都是对应模型标签': 0x01,  # 标签
}

'''
Date: 2024-02-22 13:55:46
author: zjs
description: 获取识别结果 [x,y,w,h,p,result]
0x00 结果
0x01 标签
'''

def get_res(uuidHex=util.genUuid()):
    cmd = 0x03
    cameraServiceSocket.sendall(
        util.genSendPack(cmd=cmd, subcmd=resultType['result'],uuid=uuidHex))


    def callback(hexList):
        resultLength = hexList[10]
        dateStartIndex = 14
        dateLength = 46

        resultData = hexList[dateStartIndex:dateStartIndex + dateLength * resultLength]
        resultSlice = []
        # 分片获取结果
        for index in range(0, int(len(resultData) / dateLength)):
            activeChunk = resultData[index * dateLength: index * dateLength + dateLength]
            # 位置信息和返回值
            value = activeChunk[4: 4 + activeChunk[0]].decode('utf-8')
            left, top, right, bottom = [
                activeChunk[el] | (activeChunk[el + 1] << 8)
                for el in [34, 36, 38, 40]
            ]
            # 准确度
            confBytes = activeChunk[42:46]
            conf = struct.unpack('f', confBytes)[0]

            # 将浮点数转换为百分比，并保留两位小数
            conf = round(conf * 100, 2) or 0
            resultSlice.append([
                left,
                top,
                abs(right - left),
                abs(top - bottom),
                conf,
                value,
            ])
        return resultSlice

    return waitSocketResult(uuid = (uuidHex[0]|(uuidHex[1]<<8)),cb = callback)



'''
Date: 2024-02-22 13:55:46
author: zjs
description: 获取识别结果 [(x,y,w,h,p,result)]  异步版本给js用
0x00 结果
0x01 标签
'''
def async_get_res(uuid):
    cmd = 0x03
    cameraServiceSocket.sendall(
        util.genSendPack(cmd=cmd, subcmd=resultType['result'],uuid=uuid))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取人脸标签
'''


def get_face_tags():
    cmd = 0x03
    cameraServiceSocket.sendall(
        util.genSendPack(cmd, modeType['face_detect']))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取分类标签
'''


def get_class_tags():
    cmd = 0x03
    cameraServiceSocket.sendall(
        util.genSendPack(cmd, modeType['classify']))


'''
Date: 2024-02-23 18:56:47
author: zjs
description: 获取当前模型标签
'''

def get_tags():
    return  [el[-1] for el in get_res()]

'''
Date: 2024-02-22 17:41:35
author: zjs
description: 获取rtsp 地址
'''


async def __sendRtspUrlByClient():
    await clientServiceSocket.send(udp.getRtspUrl().encode())
    await asyncio.sleep(0.05)
