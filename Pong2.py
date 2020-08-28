# Pong 유사 게임
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
import time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
matchStart = time.time()  # 경과시간 측정용 변수

rscore = 0  # 왼쪽 오른쪽 득점 저장용
lscore = 0

font = pygame.font.Font(None, 40)  # 점수 표시용 폰트
font2 = pygame.font.SysFont("corbel", 70)
font3 = pygame.font.Font(None, 60)
font4 = pygame.font.Font(None, 30)

ballImg = pygame.image.load("images/pyGameBall.png").convert_alpha()
# Class==========================================


class Bat:
    def __init__(self, ctrls, x, side):
        self.ctrls = ctrls
        self.x = x
        self.y = 260
        self.side = side
        self.lastHit = 0  # 전에 친 시간 저장용

    def move(self):
        if pressedKeys[self.ctrls[0]] and self.y > 0:
            self.y -= 10
        if pressedKeys[self.ctrls[1]] and self.y < 520:
            self.y += 10

    def hit(self):
        if time.time() > self.lastHit + 0.3:
            self.lastHit = time.time()

    def draw(self):
        # 배트가 때릴 때 선이 향하는 방향쪽으로 약간 나왔다 들어가게 하기
        # 0.05초간 왼쪽 배트의 경우 1*1(참은 1, 거짓은 0)*10, 오른쪽 배트는 -1*1*10 그 이후는 둘다 모두 0
        offset = -self.side * (time.time() < self.lastHit+0.05)*10
        pygame.draw.line(screen, (255, 255, 255),
                         (self.x+offset, self.y), (self.x+offset, self.y + 80), 6)


class Ball:
    def __init__(self):
        # 좌우 부채꼴 모양 각도의 랜덤 각 공간 지정
        self.d = (math.pi/3)*random.random() + \
            (math.pi/3)+math.pi*random.randint(0, 1)
        self.speed = 12
        self.dx = math.sin(self.d)*self.speed
        self.dy = math.cos(self.d)*self.speed
        self.x = 475
        self.y = 275

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        # 화면 위 아래에 닿고 향하는 방향이 같을 경우 y반대방향으로 방향전환
        if (self.y <= 0 and self.dy < 0) or (self.y >= 550 and self.dy > 0):
            self.dy *= -1
            # atan2를 이용해 dx, dy값으로 각도 알아내기
            self.d = math.atan2(self.dx, self.dy)
        # 배트에 닿을 경우 x반대방향으로 방향전환
        for bat in bats:
            # 배트와 볼의 사각 충돌 감지 & 진행방향과 닿는 배트의 side가 같은 경우만 튕기기
            # side 체크를 하는 이유는 공이 배트에서 지그재그로 튀는 버그 방지책
            if pygame.Rect(bat.x, bat.y, 6, 80).colliderect(self.x, self.y, 50, 50) \
                    and abs(self.dx)/self.dx == bat.side:
                # 튕기는 방향에 작은 각도를 랜덤하게 추가(-22.5도~22.5도 사이 임의의 각)
                self.d += random.random()*math.pi/4 - math.pi/8
                # 새로 만든 각이 너무 수직에 가까울 경우 배제.
                # 새로 만든 각이 너무 오른쪽이면 d를 오른쪽으로 조금 돌리고
                if(0 < self.d < math.pi/6) or (math.pi * 5/6 < self.d < math.pi):
                    self.d = ((math.pi/3)*random.random() + (math.pi/3))
                # 각이 너무 왼쪽이면 왼쪽으로 조금 돌린 뒤
                elif(math.pi < self.d < math.pi*7/6) or (math.pi*11/6 < self.d < math.pi*2):
                    self.d = ((math.pi/3)*random.random()+(math.pi/3))+math.pi
                self.d *= -1  # 각에 -1 곱해 반대방향 만들고
                self.d %= math.pi*2  # 각의 크기를 2pi로 모듈러해서 양수로 만든다
                # 속도가 20이하면 약간 속도 높이기
                # if self.speed < 20:
                #    self.speed * 1.1
                # 공을 배트로 칠때마다 속도 늘리기
                if time.time() < bat.lastHit + 0.05 and self.speed < 20:
                    self.speed *= 1.5
                # dx, dy를 새로 만든 각에 맞춰 다시 계산
                self.dx = math.sin(self.d)*self.speed
                self.dy = math.cos(self.d)*self.speed

    def draw(self):
        screen.blit(ballImg, (self.x, self.y))


# List==========================================
ball = Ball()
bats = [Bat([K_a, K_z], 10, -1), Bat([K_UP, K_DOWN], 984, 1)]
# Game Loop==========================================
while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_q:
                bats[0].hit()
            if event.key == K_LEFT:
                bats[1].hit()
    pressedKeys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))
    # 배경 그리기
    # line(그릴 곳, 색, 선 시작위치, 선 끝위치, 두께)
    pygame.draw.line(screen, (155, 155, 155), (screen.get_width()/2, 80),
                     (screen.get_width()/2, screen.get_height()), 3)
    # circle(그릴 곳, 색, 원의 중앙 위치, 원 크기, 두께)
    pygame.draw.circle(screen, (255, 255, 255),
                       (int(screen.get_width()/2), int(screen.get_height()/2)),
                       50, 3)
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
    screen.blit(txt, (screen.get_width()-20-txt.get_width(), 20))
    # 시계 표시
    # time.time()-matchStart은 프로그램 시작 후 경과 시간
    # 남은시간 표시는 60-(time.time()-matchStart)로 구할 수 있다
    txt = font.render(str(int(time.time()-matchStart)), True, (255, 255, 255))
    screen.blit(txt, (screen.get_width()/2 - txt.get_width()/2, 20))
    # 엔딩화면 표시
    if rscore > 2 or lscore > 2:  # 한 쪽이 3점 이상 득점시
        # if time.time() - matchTime > 60: #게임 시작 후 60초 경과시
        txt = font2.render("Score", True, (255, 0, 255))
        screen.blit(txt, (screen.get_width()/4 -
                          txt.get_width()/2, screen.get_height()/4))
        screen.blit(txt, (screen.get_width()*3/4 -
                          txt.get_width()/2, screen.get_height()/4))
        txt = font3.render(str(lscore), True, (255, 255, 255))
        screen.blit(txt, (screen.get_width()/4 -
                          txt.get_width()/2, screen.get_height()/2))
        txt = font3.render(str(rscore), True, (255, 255, 255))
        screen.blit(txt, (screen.get_width()*3/4 -
                          txt.get_width()/2, screen.get_height()/2))
        txt = font4.render("Press Space to Restart", True, (255, 255, 255))
        screen.blit(txt, (screen.get_width()*5/9, screen.get_height()-100))
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            # 스페이스 키 누르면 루프 탈출, 탈출전 변수들 초기화가 필요
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                lscore = rscore = 0
                bats[0].y = bats[1].y = 200
                matchStart = time.time()
                ball = Ball()
                break
            pygame.display.update()

    # 업데이트
    pygame.display.update()
