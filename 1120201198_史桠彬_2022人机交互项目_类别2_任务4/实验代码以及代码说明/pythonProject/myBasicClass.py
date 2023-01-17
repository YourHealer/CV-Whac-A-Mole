# 调用operator库，实现函数式编程
import operator
# 调用random库，实现随机化
from random import Random
# 调用functools库，实现累加操作
from functools import reduce
# 调用PyQt5库，实现计算机操作用户界面
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QCursor

# 定义场景类
class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # 读取地坑和地鼠形象
        self.background = QPixmap(r".\img\hole.png")
        self.mole = QPixmap(r".\img\mouseExisting.png")

        # 定义数组存储图元
        self.items = []

        # 设定场景中地坑的行列数
        self.rows = 4      #行数
        self.vols = 6      #列数

        # 对数组进行操作
        for y in range(self.rows):
            self.items.append([])
            for x in range(self.vols):
                mp = MyPixmapItem(parent)
                mp.setPos(mp.boundingRect().width()*x, mp.boundingRect().height()*y)
                self.addItem(mp)
                self.items[y].append(mp)

        # 设定游戏时间为60秒
        self.count = 60

        # 创建计时器
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.refresh)
        self.timer.timeout.connect(self.showMole)

    # 用于启动游戏的函数
    def gameStart(self):
        #  开启定时器
        self.timer.start(2000)
        self.timer2.start(1000)
        for item in reduce(operator.add, self.items):
            item.start = True

    # 用于暂停游戏的函数
    def gamePause(self):
        # 暂停定时器
        self.timer.stop()
        for item in reduce(operator.add, self.items):
            item.start = False

    # 用于终止游戏的函数
    def gameStop(self):
        for item in reduce(operator.add, self.items):
            item.setPixmap(self.background)
            item.isMole = False
            item.start = False
        self.timer.stop()
        self.parent.score = 0
        self.parent.lcdNumber_score.display(self.parent.score)

    # 随机出现地鼠
    def showMole(self):
        # 对数组的每一个元素初始设定为无地鼠的单地洞状态
        for item in reduce(operator.add, self.items):
            # 设置地洞背景图片
            item.setPixmap(self.background)
            # 设置没有地鼠
            item.isMole = False

        # 设置每次出现随机位置出现2-4只地鼠
        for i in range(Random().randint(2, 4)):
            x = Random().randint(0, self.vols - 1)
            y = Random().randint(0, self.rows - 1)
            self.items[y][x].setPixmap(QPixmap(self.mole))
            self.items[y][x].isMole = True

    # 刷新
    def refresh(self):
        # 时间有余，游戏继续
        if self.count > 0:
            self.parent.lcdNumber_time.display(self.count)
            self.count -= 1
        # 时间用尽，游戏结束
        else:
            self.timer2.stop()
            QtWidgets.QMessageBox.information(self.parent,'提示','时间到，您最后的得分为' + str(self.parent.score))
            # 重置设定
            self.count = 60
            for item in reduce(operator.add, self.items):
                item.setPixmap(self.background)
                item.isMole = False
                item.start = False
            self.timer.stop()
            self.parent.score = 0
            self.parent.lcdNumber_score.display(self.parent.score)

# 定义图元类
class MyPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent):
        super().__init__()
        self.setPixmap(QPixmap(r".\img\hole.png"))
        self.setCursor(QCursor(QPixmap("./img/hammerPreparing.png")))

        self.parent = parent

        self.__isMole = False       # 标识图片是否是老鼠
        self.__start = False        # 标识游戏是否正在进行中

    @property
    def isMole(self):
        return self.__isMole

    @isMole.setter
    def isMole(self,value):
        self.__isMole = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    def mousePressEvent(self, event):
        # QtWidgets.QMessageBox().question(None, "提示", "鼠标按下", QtWidgets.QMessageBox.Yes)   # 注意None不能是self。
        self.setCursor(QCursor(QPixmap('./img/hammerUsing.png')))
        if self.__start:
            if self.__isMole == True:
                self.__isMole = False
                # playsound(r'./sound/hit.mp3')
                self.parent.score += 10
                self.setPixmap(QPixmap(r".\img\mouseHitting.png"))
                self.parent.lcdNumber_score.display(self.parent.score)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.setCursor(QCursor(QPixmap("img/hammerPreparing.png")))
