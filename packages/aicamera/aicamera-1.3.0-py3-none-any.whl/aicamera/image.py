import time
import os
import cv2
from . import rtsp

'''
Date: 2024-02-22 11:01:55
author: zjs
description: 从摄像头获取一张图片
'''


def take_photo():
    return rtsp.getCurrentFrame()


'''
Date: 2024-02-22 11:05:23
author: zjs
description: 保存图片
'''


def save(imaData, imgName=f'{time.time()}.jpg'):
    if not imgName.endswith('.jpg'):
        imgName += '.jpg'
    saveFile = os.path.normpath(os.path.join(os.getcwd(), imgName))
    # 没有路径创建路径
    saveDir = os.path.dirname(saveFile)
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    cv2.imwrite(saveFile, imaData)
    return imgName
