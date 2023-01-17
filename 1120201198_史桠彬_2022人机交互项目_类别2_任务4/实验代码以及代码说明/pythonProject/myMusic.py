import pygame
# 音乐的路径
file=r".\music\mus.mp3"
# 初始化
pygame.mixer.init()
# 加载音乐文件
track = pygame.mixer.music.load(file)
# 开始播放音乐流
pygame.mixer.music.play()
