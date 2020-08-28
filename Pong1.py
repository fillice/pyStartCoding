# Pong 유사 게임 기본 작동
# 공은 중앙에서 랜덤한 각도로 좌/우로 날아간다.
# 화면 위/아래에 닿으면 반대 방향으로 날아간다.
# 좌우의 배트에 맞으면 반대 방향으로 날아간다.
# 공이 화면 좌우로 빠져 나갈 경우 점수 올리고 중앙에서 공 새로 생성하기.
# 사용한 공 그림 크기: 50*50
# Setup==========================================
import pygame
import sys
import math
import random
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

rscore = 0  # 왼쪽 오른쪽 득점 저장용
lscore = 0

font = pygame.font.Font(None, 40)  # 점수 표시용 폰트

ballImg = pygame.image.load("images/pyGameBall.png").convert_alpha()
# Class==========================================


class Bat:
    def __init__(self, ctrls, x):
        self.ctrls = ctrls
        self.x = x
        self.y = 260

    def move(self):
        if pressedKeys[self.ctrls[0]] and self.y > 0:
            self.y -= 10
        if pressedKeys[self.ctrls[1]] and self.y < 520:
            self.y += 10

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255),
                         (self.x, self.y), (self.x, self.y + 80), 6)


class Ball:
    def __init__(self):
        d = (math.pi/3)*random.random() + \
            (math.pi/3)+math.pi*random.randint(0, 1)
        self.dx = math.sin(d)*12
        self.dy = math.cos(d)*12
        self.x = 475
        self.y = 275

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        screen.blit(ballImg, (self.x, self.y))

    def bounce(self):
        # 화면 위 아래에 닿을 경우 y반대방향으로 방향전환
        if self.y <= 0 or self.y >= 550:
            self.dy *= -1
        # 배트에 닿을 경우 x반대방향으로 방향전환
        for bat in bats:
            # 배트와 볼의 사각 충돌 감지
            if pygame.Rect(bat.x, bat.y, 6, 80).colliderect(self.x, self.y, 50, 50):
                self.dx *= -1


# List==========================================
ball = Ball()
bats = [Bat([K_a, K_z], 10), Bat([K_UP, K_DOWN], 984)]
# Game Loop==========================================
while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    pressedKeys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))
    # 배트 움직임/그리기 처리
    for bat in bats:
        bat.move()
        bat.draw()
    # 볼이 화면 좌우로 나간 경우 득점 올리고 새 볼 생성
    if ball.x < -50:
        ball = Ball()
        rscore += 1
    if ball.x > 1000:
        ball = Ball()
        lscore += 1
    # 볼 이동과 그리기 튕기기 처리
    ball.move()
    ball.draw()
    ball.bounce()
    # 점수 표시
    txt = font.render(str(lscore), True, (255, 255, 255))
    screen.blit(txt, (20, 20))
    txt = font.render(str(rscore), True, (255, 255, 255))
    screen.blit(txt, (980-txt.get_width(), 20))
    # 업데이트
    pygame.display.update()
