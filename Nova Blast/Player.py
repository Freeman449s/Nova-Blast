import time, librosa
from threading import Thread
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # 关闭pygame欢迎消息
import pygame

import Global


class Player(Thread):
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path

    def run(self):
        while not Global.c.acquire():
            continue
        length = int(librosa.get_duration(filename=self.path))  # 音乐长度（秒）
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
        Global.playStartTime = time.time()
        Global.nextBeatTime += Global.playStartTime
        Global.c.notify()  # 继续绘制
        Global.c.release()
        time.sleep(length)
