# '파이썬으로 시작하는 코딩' 18장 돌연변이 바이오드론 따라하기
# 파리 랜덤 위치/방향으로 생성과
# 향하는 방향으로 이동하기,
# 화면밖으로 나가면 제거하기
# 파리 png 사이즈: 50*50

import pygame
import sys
import time
import random
import math
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Fly Catcher")
screen = pygame.display.set_mode((1000, 600))
flyImg = pygame.image.load("images/pygameFly.png").convert_alpha()
spawnTime = time.time()


class Fly:
    def __init__(self):
        self.x = random.randint(0, screen.get_width()-flyImg.get_width())
        self.y = random.randint(0, screen.get_height()-flyImg.get_height())
        self.dir = random.randint(0, 359)
        self.dx = -math.sin(math.radians(self.dir))*2
        self.dy = -math.cos(math.radians(self.dir))*2

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def offScreen(self):
        return (self.y > screen.get_height()+flyImg.get_height() or
                self.y < 0-flyImg.get_height() or
                self.x > screen.get_width()+flyImg.get_width() or
                self.x < 0-flyImg.get_height())

    def draw(self):
        #rotate(회전대상, 회전각도)
        rotated = pygame.transform.rotate(flyImg, self.dir)
        screen.blit(rotated, (self.x+flyImg.get_width()/2-rotated.get_width()/2,
                              self.y+flyImg.get_height()/2-rotated.get_height()/2))


flys = []

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    if time.time() - spawnTime > 0.5:
        flys.append(Fly())

    screen.fill((255, 255, 255))

    i = 0
    while i < len(flys):
        flys[i].draw()
        flys[i].move()
        if flys[i].offScreen():
            del flys[i]
            i -= 1
        i += 1
    print(len(flys))  # 현재 파리 수 확인용

    pygame.display.update()
