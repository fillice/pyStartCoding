# 비내리는 효과
# Setup======================================
import pygame
import sys
import random
from pygame.locals import *

pygame.init()  # pygame 초기화
pygame.display.set_caption("Rain")  # 게임 윈도우에 제목 넣기
screen = pygame.display.set_mode((1000, 600))  # 화면 크기 정하기
clock = pygame.time.Clock()  # 시간 조정용

'''rainY = 0
rainX = random.randint(0, 1000)'''
# raindropSpawnTime = 0

# Class==========================================

class Raindrop:
    def __init__(self):  # 초기화
        # 0~1000 범위 내 무작위 x위치로 정하기
        self.x = random.randint(0, 1000)
        self.y = -5
        # 각 빗방울 낙하속도 랜덤으로 하기
        self.speed = random.randint(5, 18)

    def move(self):  # 이동 관련
        self.y += self.speed

    def draw(self):  # 화면에 그리기 관련
        # line(그려질 곳, 색, 직선 시작좌표xy, 직선 끝좌표xy, 직선 두께)
        pygame.draw.line(screen, (155, 155, 155), (self.x, self.y),
                         (self.x, self.y+5), 1)

    def offScreen(self):  # 화면 밖으로 나갔는지 판단용
        return self.y > 800


# List===========================================
raindrops = []
# Game Loop======================================
while 1:
    clock.tick(60)
    # 나가기 입력 받으면 루프 탈출
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for r in range(0, 15):
        raindrops.append(Raindrop())
    screen.fill((5, 5, 55))  # 화면 색으로 채우기
    '''rainY += 4
    pygame.draw.line(screen, (0, 0, 0), (rainX, rainY), (rainX, rainY+5), 1)'''
    '''for raindrop in raindrops:
        raindrop.move()
        raindrop.draw()'''
    i = 0
    while i < len(raindrops):
        raindrops[i].move()
        raindrops[i].draw()
        if raindrops[i].offScreen():
            del raindrops[i]  # 리스트에서 항목 제거
            i -= 1
        i += 1

    pygame.display.update()  # 변화들 업데이트
