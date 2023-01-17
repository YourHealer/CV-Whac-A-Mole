# 调用cv2库，完成图像处理与识别
import cv2
# 调用numpy库，处理数组数据
import numpy as np
# 调用PyQt5库，实现计算机操作用户界面
from PyQt5.QtGui import *

# 用于进行图片转换的函数
def convertImg(cvImg):
    cvImg = cvImg.astype(np.uint8)
    hei, wid, cha = cvImg.shape[:3]
    cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    cvImg = QImage(cvImg.data, wid, hei, wid * cha, QImage.Format_RGB888)

    return cvImg

# 用于进行大小重置的函数
def resizeImg(img, wid, hei):
    weight = np.array(img).shape[1]
    height = np.array(img).shape[0]

    if weight / wid >= height / hei:
        ratio = weight / wid
    else:
        ratio = height / hei
    newWid = int(weight / ratio)
    newHei = int(height / ratio)

    return newWid,newHei
