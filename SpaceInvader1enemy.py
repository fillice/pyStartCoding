
# Setup==========================================
import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((640, 650))
clock = pygame.time.Clock()
lastEnemySpawnTime = 0

enemyImg = pygame.image.load("images/pygameEnemy1.png").convert_alpha()
#Class==========================================
class Enemy: #적 관련
    def __init__(self): #초기화
        #self.x = random.randint(0, 570)
        self.x = 285
        self.y = -100
        self.dy = random.randint(2, 6)
        self.dx = random.choice((-1, 1)) * self.dy
    def move(self): #이동 관련
        self.x += self.dx
        self.dy += 0.01
        self.y += self.dy
        # if self.y > 150 and self.y < 250:
        #     self.x += 5
        # if self.y >250:
        #     self.x -= 5
    # 화면 좌우로 나가면 x 진행방향 바꾸기
    def bounce(self):
        if self.x < 0 or self.x > 570: 
            self.dx *= -1
    #적이 화면 아래로 나갔는지 체크
    def offScreen(self): 
        return self.y > 640
    def draw(self): #화면에 그리기
        screen.blit(enemyImg, (self.x, self.y))
# List==========================================
enemies = []
# Game Loop==========================================
while 1:
    clock.tick(60) #시간 인터벌 설정
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    # 0.5초 마다 새 적을 리스트에 추가시키기
    if time.time() - lastEnemySpawnTime > 0.5:
        enemies.append(Enemy())
        lastEnemySpawnTime = time.time()

    screen.fill((0,0,0)) #화면 검은색으로 칠하기

    i = 0
    while i < len(enemies):
        enemies[i].move() #적 이동
        enemies[i].bounce() #적 좌우 화면 이탈시 방향 바꾸기
        enemies[i].draw() #적 화면에 그리기
        if enemies[i].offScreen(): #화면 아래로 나간 적 제거하기
            del enemies[i]
            i -= 1
        i += 1

    pygame.display.update() #모든 변화 업데이트