# 비내리는 효과 + 이미지 불러오기
# Setup======================================
import pygame, sys, random, time
from pygame.locals import *

pygame.init()  # pygame 초기화
pygame.display.set_caption("Rain")  # 게임 윈도우에 제목 넣기
screen = pygame.display.set_mode((1000, 600))  # 화면 크기 정하기
clock = pygame.time.Clock()  # 시간 조정용
lastHitTime = 0 #최종 충돌 시간 저장용

#이미지 불러와 컴 그래픽 카드가 읽을 수 있는 포맷으로 전환
tmanImg = pygame.image.load("images/tmanUmbrella.png").convert_alpha()
tmanNotUmImg = pygame.image.load("images/tmanUmbrellaNot.png").convert_alpha()
cloudImg = pygame.image.load("images/cloud.png").convert_alpha()

# Class==========================================
#변화 테스트

class Raindrop:
    def __init__(self, x, y):  # 초기화
        self.x = x
        self.y = y
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

class Tman:
    def __init__(self):
        self.x = 300
        self.y = 400
    def draw(self):
        #지난 충돌시간 이후 1초 이상 경과되었으면
        if time.time() < lastHitTime + 1:
            #이미지 화면에 전송 blit(전송할 이미지, 전송 xy좌표)
            screen.blit(tmanImg, (self.x, self.y))
        else:
            screen.blit(tmanNotUmImg, (self.x, self.y))
    #빗방울과의 충돌처리
    def hitBy(self, raindrop):
        #보이지 않는 직사각형 만들고 빗방울과 충돌여부 체크, 충돌시 True 반환
        return pygame.Rect(self.x, self.y, 135, 155).collidepoint((raindrop.x, raindrop.y))

class Cloud:
    def __init__(self):
        self.x = 300
        self.y = 50
    def draw(self): # 이미지 화면에 전송하기
        screen.blit(cloudImg, (self.x, self.y))
    def move(self): # 키보드에 따라 이동 처리
        if pressedKeys[K_RIGHT]:
            self.x += 1
        if pressedKeys[K_LEFT]:
            self.x -= 1
    #구름 아래 빗방울 인스턴스 생성하고 리스트에 추가
    def rain(self):
        for i in range(3):
            raindrops.append(Raindrop(random.randint(self.x, self.x+175), self.y + 60))

# List===========================================
raindrops = [] #빗방울 인스턴스들 담을 리스트 생성
tman = Tman() #인스턴스 만들기
cloud = Cloud()
# Game Loop======================================
while 1:
    clock.tick(60)
    # 나가기 입력 받으면 루프 탈출
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    #구름 조종용 입력 처리용
    pressedKeys = pygame.key.get_pressed()

    screen.fill((5, 5, 55))  # 화면 색으로 채우기
    tman.draw() # tman 그리기
    cloud.draw() # 구름 그리기
    cloud.rain() # 빗방울 생성, 리스트 추가시키기
    cloud.move() # 구름 이동

    i = 0
    while i < len(raindrops):
        raindrops[i].move()
        raindrops[i].draw()
        #화면밖으로 나가거나 tman과 충돌시 제거
        if raindrops[i].offScreen():
            del raindrops[i]  # 리스트에서 항목 제거
            i -= 1
        elif tman.hitBy(raindrops[i]):
            del raindrops[i]  # 리스트에서 항목 제거
            lastHitTime = time.time()
            i -= 1
        i += 1

    pygame.display.update()  # 변화들 업데이트
