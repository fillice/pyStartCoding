import pygame  # 파이썬을 위한 미술도구 불러오기
import sys  # 파이썬 실행시키는 컴 시스템 부분과 파이썬이 대화 가능하게 함
import time  # time 사용하기 위해 불러옴
from pygame.locals import *  # 파이게임의 함수들을 한번에 모두 준비시키기

pygame.init()  # pygame 초기화
pygame.display.set_caption("First Program")  # 게임 윈도우에 제목 넣기
screen = pygame.display.set_mode((640, 480))  # 화면 크기 정하기
xpos = 100
ypos = 200
clock = pygame.time.Clock()  # 시간 조정용

while 1:  # 무한루프
    # 속도를 고정시키기 위해 1/60초당 1번 루프 실행하게 지정
    clock.tick(60)
    # 나가기 입력을 받으면 루프 탈출
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # 눌린 키에따라 좌우 이동시키기
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_RIGHT]:
        xpos += 3
    if pressedKeys[K_LEFT]:
        xpos -= 3
    if pressedKeys[K_UP]:
        ypos -= 3
    if pressedKeys[K_DOWN]:
        ypos += 3

    screen.fill((255, 255, 255))  # 화면 흰색으로 채우기
    # 원 그리기: circle(그려질 곳, 원의 색, xy위치, 원의 반지름, (테두리 두께))
    # pygame.draw.circle(screen, (0, 255, 0), (xpos, ypos), 20)
    # 번쩍이게 하기
    # time.time()%1은 0~1사이 값이 나오는데 그중 0.5이하면 그리지 않으니
    # 1초당 한번 원이 나타났다 사라졌다를 반복하는 듯 표현된다
    if time.time() % 1 < 0.5:
        pygame.draw.circle(screen, (0, 255, 0), (xpos, ypos), 20)
    pygame.display.update()  # 변화들을 화면에 표시
