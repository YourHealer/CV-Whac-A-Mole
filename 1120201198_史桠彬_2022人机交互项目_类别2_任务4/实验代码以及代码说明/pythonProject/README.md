# 【打地鼠】支持手势识别版

## 操作教程

### 配置说明

#### 软件
Anaconda 1.7.2 + Python 3.7.3 + PyCharm + Windows 10

【Jupyter Notebook同理 后续以PyCharm为例说明】

#### 库
1. mediapipe
2. functools
3. operator
4. random
5. autopy
6. pygame
7. pyqt5
8. numpy
9. sys
10. cv2

【高效调用单库】

Pycharm - Terminal - 输入“pip install **库名** -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com”


### 运行说明

1.  通过“Open Folder as PyCharm Community Edition Project”打开本文件夹。
2.  运行 mainFunction.py 程序。


### 游戏说明

#### 游戏规则
【贪吃的地鼠们又来啃农民伯伯的田啦！快来帮农民伯伯打地鼠吧！】

- 游戏界面内每次随机出现2-4只地鼠，狡猾的地鼠们每次只会露头两秒钟。你需要在地鼠露头期间用木锤将它们击晕，每击晕一只地鼠你将会获得10分。

- 通过不同的手势，脱离鼠标实现移动木锤和敲击木锤。

#### 界面说明

- 开始：启动游戏。

- 暂停：页面静止，点击【开始】后游戏继续。

- 停止：结束游戏。

#### 操作说明
- 伸出食指，收回中指（呈现“1”的手势）：在游戏界面外移动鼠标，在游戏界面内移动木锤。
- 伸出食指，伸出中指（呈现“2”的手势）：在游戏界面外单击鼠标左键，在游戏界面内敲击木锤。


### 注意事项
- 在开始游戏前，请放大游戏窗口，以获得广阔的游戏场景。
- 在开始游戏前，请移动窗口滚轮，以获得方便的操作区域。
- 在操作过程中，若要实现“敲击木锤”，请将伸出的食指与中指尽量靠拢，以获得良好的交互体验。
- 程序附有音乐，请打开扬声系统，以获得更好的游戏体验。

### 版权声明

#### 图片
- 千库网-在土坑探出脑袋的鼹鼠
- 千库网-天使光环翅膀素材
- 站网-小星星徽章练习

#### 音乐
- 久石让-Summer