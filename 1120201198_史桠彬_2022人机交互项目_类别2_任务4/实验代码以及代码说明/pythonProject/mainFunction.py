# 调用system库，创建窗口进行交互
import sys
# 调用PyQt5库，实现计算机操作用户界面
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# 调用mediapipe库，对手部关键点进行检测
import mediapipe as mp
# 调用autopy库，完成鼠标模拟操作
import autopy
# 调用cv2库，完成图像处理与识别
import cv2
# 调用numpy库，处理数组数据
import numpy as np

import myBasicClass
from handInfoFunctions import *
import LogIn
import preFunction
import myMusic

# 定义线程类
class myThread(QThread):
    # 自定义信号对象。同时允许该信号传递一个字符串
    myFlag = pyqtSignal(str)

    # 调用父函数
    def __init__(self):
        super(myThread, self).__init__()

    # 重写run方法，启用多线程
    def run(self):  # 线程执行函数
        pass

# 定义窗口类
class myWindow(QMainWindow, LogIn.uiForLogIn):
    def __init__(self):
        # 初始化窗口
        super(myWindow, self).__init__()

        # 对界面初始化
        self.setupUi(self)

        # 对场景初始化
        self.scene = myBasicClass.MyScene(self)
        self.graphicsView.setScene(self.scene)
        self.initialAll()

        # 实例化线程对象
        self.mythread = myThread()
        self.score = 0

        # 绑定信号
        self.pushButton_start.clicked.connect(self.scene.gameStart)
        self.pushButton_pause.clicked.connect(self.scene.gamePause)
        self.pushButton_stop.clicked.connect(self.scene.gameStop)
        self.timer.timeout.connect(self.setCamera)

# 用于初始化屏幕、摄像头等
    def initialAll(self):
        # 自行获取屏幕宽和高
        self.screenWid, self.screenHei = autopy.screen.size()
        # 指定摄像头宽度和高
        self.cameraWid, self.cameraHei = 640, 480
        # 定义鼠标移动参数
        self.smoothening = 5
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        # 用于绘制
        self.mpDraw = mp.solutions.drawing_utils

        # 用于人手检测，初始化为检测目标为单手，手部检测模型的最小置信度值为0.7，地标跟踪模型的最小置信度值为0.5
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

        # 用于读取电脑内置默认摄像头
        self.cap = cv2.VideoCapture()
        self.cap.open(0)
        # 用于设置摄像头参数
        self.cap.set(3, self.cameraWid)  # width=1920
        self.cap.set(4, self.cameraHei)  # height=1080

        # 用于设置定时器，初始化为每30ms更新一次
        self.timer = QTimer()
        self.timer.start(30)

# 用于读取摄像头信息
    def setCamera(self):
        # 从摄像头中读取信息（是否读取到图片，截取到的各帧图片）
        ret, self.image = self.cap.read()
        # 获取图像的垂直尺寸、水平尺寸、通道数目
        hei, wid, cha = self.image.shape[0], self.image.shape[1], self.image.shape[2]
        # 水平翻转图片
        frame = cv2.flip(self.image, 1)
        # 转换图片的颜色空间
        imageSpace = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 获取图片的人手信息
        info = self.hands.process(imageSpace)
        myInfo = info.multi_hand_landmarks
        # 对人手信息进行判断
        if myInfo:
            # 根据信息绘制检测出的单手
            self.mpDraw.draw_landmarks(frame, myInfo[0], self.mpHands.HAND_CONNECTIONS)
            # 获取手部关节坐标
            handPointList = getHandPoint(info, hei, wid)
            # 通过手部关节坐标判断手势
            myHandPose = judgeHandPose(handPointList)

            # 对手势进行判断
            if myHandPose == 'Gesture1':
                # 释放鼠标左键
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
                # 将摄像头的长和宽映射到屏幕的长和宽
                screen_x = np.interp(handPointList[8][0], (50, self.cameraWid - 100), (0, self.screenWid))
                screen_y = np.interp(handPointList[8][1], (50, self.cameraHei - 100), (0, self.screenHei))
                # 平滑鼠标移动
                self.clocX = self.plocX + (screen_x - self.plocX) / self.smoothening
                self.clocY = self.plocY + (screen_y - self.plocY) / self.smoothening
                autopy.mouse.move(self.clocX, self.clocY)
                self.plocX, self.plocY = self.clocX, self.clocY
                cv2.circle(frame, (handPointList[8][0], handPointList[8][1]), 10, (255, 0, 255), cv2.FILLED)

            elif myHandPose == 'Gesture2':
                # 根据手部节点坐标判断移动距离：
                if np.sqrt(np.square(handPointList[8][0] - handPointList[12][0]) + np.square(handPointList[8][1] - handPointList[12][1])) < 50:
                    # 点击鼠标左键
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
                    # 画圆
                    cv2.circle(frame, (int((handPointList[8][0] + handPointList[12][0]) / 2), int((handPointList[8][1] + handPointList[12][1]) / 2)), 10, (0, 255, 0), cv2.FILLED)

        # 获取新的宽和高
        newWid, newHei = preFunction.resizeImg(frame, wid = self.label_cap.width(), hei = self.label_cap.height())
        # 在控件里显示图片
        self.label_cap.setPixmap(QPixmap.fromImage(preFunction.convertImg(frame).scaled(newWid, newHei, Qt.KeepAspectRatio)))
        self.label_cap.setAlignment(Qt.AlignCenter)  #

    # 让窗口显示在屏幕中间
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        # 获取位置信息
        newLeft = int((screen.width()-self.geometry().width())/2)
        newTop = int((screen.height()-self.geometry().height())/2-40)
        # 将窗口置于屏幕中间
        self.move(newLeft,newTop)

# 运行主函数即可开始游戏
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建MyWindow对象
    MainWindow = myWindow()
    # 调用center（）方法，使窗口呈现在中间
    MainWindow.center()
    # 调用show（）方法，执行程序
    MainWindow.show()
    # 循环结束退出程序
    sys.exit(app.exec_())

