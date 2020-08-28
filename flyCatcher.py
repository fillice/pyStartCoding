# '파이썬으로 시작하는 코딩' 파리 잡기 게임 따라하기
# 게임 모드는 시작화면/게임화면/게임오버화면으로 구성
# 파리 랜덤 위치/방향으로 생성
# 개구리 혀 내밀어 파리와 닿으면 파리 끌어와 먹고 에너지 증가
# 개구리 에너지는 시간따라 점차 감소, 0이하 되면 게임오버
# 게임 중 에너지바, 실행시간 표시
# 게임 오버시 재시작 처리
# png 사이즈 파리: 50*50 개구리: 100 * 100, 시작화면/게임오버화면: 400*300
# 파리 소리: 1.4초간 재생
#Setup#############################################
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
font1 = pygame.font.SysFont("draglinebtndm", 60)
font2 = pygame.font.SysFont("couriernew", 15)

menu = "start"
deathTime = False

startScreenImg = pygame.image.load("images/pygameFlyStart.png").convert_alpha()
gameoverImg = pygame.image.load("images/pygameFlyOver.png").convert_alpha()
flyImg = pygame.image.load("images/pygameFly.png").convert_alpha()
frogImg = pygame.image.load("images/pygameFrog.png").convert_alpha()
flySnd = pygame.mixer.Sound("sounds/fly-buzz.ogg")
tongueSnd = pygame.mixer.Sound("sounds/tongue.ogg")

#Class#############################################


class Frog:
    def __init__(self):
        self.dir = 0
        self.tongueDist = 0
        self.tongueExtend = 0
        self.energy = 100

    def move(self):
        # 혀 길이는 혀 뻗는 정도 * 10, 0이면 계속 0, 1이면 10씩 늘어나고 -1이면 -10씩 줄어든다
        self.tongueDist += self.tongueExtend * 10
        # 혀 길이가 개구리에서 파리까지의 거리보다 더 길어지면 다시 작아지게 처리
        if self.tongueDist**2 > (fly.x-screen.get_width()/2)**2 + (fly.y-screen.get_height()/2)**2:
            self.tongueExtend = -1
        # 혀 길이가 0이하면 더이상 줄어들어 반대쪽으로 가지 않게 처리
        if self.tongueDist <= 0:
            self.tongueExtend = 0
        # 개구리 회전(혀 길이 0이하일때만 회전 가능)
        if self.tongueDist <= 0:
            if pressedKeys[K_LEFT]:
                self.dir += 4
            if pressedKeys[K_RIGHT]:
                self.dir -= 4

    # 혀끝 위치 구하기
    def getTonguePos(self):
        return(int(screen.get_width()/2-self.tongueDist*math.sin(math.radians(self.dir))),
               int(screen.get_height()/2-self.tongueDist*math.cos(math.radians(self.dir))))

    # 혀 뻗기
    def tonguePoke(self):
        if self.tongueDist <= 0:
            self.tongueExtend = 5
            tongueSnd.play()

    def draw(self):
        if deathTime:  # 개구리 죽으면 작아지다가 없어짐
            # rotozoom(이미지, 60분법 회전각, 이미지 크기에 곱할 수)
            rotated = pygame.transform.rotozoom(
                frogImg, self.dir, 1-((time.time()-deathTime)/2))
            screen.blit(rotated, (screen.get_width()/2-rotated.get_width()/2,
                                  screen.get_height()/2-rotated.get_height()/2))
        else:  # 개구리가 살아있을 때
            tpos = self.getTonguePos()  # 혀끝 위치
            # 혀끝 원 그리기
            pygame.draw.circle(screen, (255, 50, 50), tpos, 10)
            # 혀 그리기
            pygame.draw.line(screen, (255, 50, 50),
                             (screen.get_width()/2, screen.get_height()/2), tpos, 10)
            # 개구리 그리기
            rotated = pygame.transform.rotate(frogImg, self.dir)
            screen.blit(rotated, (screen.get_width()/2-rotated.get_width()/2,
                                  screen.get_height()/2-rotated.get_height()/2))


class Fly:
    def __init__(self):
        self.x = random.randint(0, screen.get_width()-flyImg.get_width())
        self.y = random.randint(0, screen.get_height()-flyImg.get_height())
        self.dir = random.randint(0, 359)
        self.spawnTime = time.time()
        flySnd.play()  # 파리 소리 재생
        self.stuck = False

    # 파리가 개구리 혀에 붙었는지 판정
    def stick(self):
        # 이미 잡혀있는 상태가 아니고 파리가 화면에 보이는 동안에만 판정
        if (not self.stuck and
                time.time() > self.spawnTime + 1.4 and time.time() < self.spawnTime + 3.4):
            tpos = frog.getTonguePos()  # 개구리 혀 위치
            fpos = (self.x+flyImg.get_width()/2, self.y +
                    flyImg.get_height()/2)  # 파리 위치
            # 혀의 끝 위치 x제곱 + y제곱 값이 (파리 중심+혀끝 원 반지름인 10)보다 작으면 혀에 붙었다 판정
            if(tpos[0]-fpos[0])**2+(tpos[1]-fpos[1])**2 < (flyImg.get_width()/2+10)**2:
                self.stuck = True

    def draw(self):
        # 개구리 혀에 붙은 경우 개구리 혀의 움직임을 따라간다
        if self.stuck:
            tpos = frog.getTonguePos()
            screen.blit(
                flyImg, (tpos[0]-flyImg.get_width()/2, tpos[1]-flyImg.get_height()/2))
        # 파리 생성 이후 1.4초 뒤 첫 조건 충족, 3.4초 뒤 둘째 조건 충족
        # 따라서 생성 뒤 1.4~3.4초의 2초간만 화면에 표시
        elif time.time() > self.spawnTime+1.4 and time.time() < self.spawnTime+3.4:
            # rotate(회전대상, 회전각도)
            rotated = pygame.transform.rotate(flyImg, self.dir)
            screen.blit(rotated, (self.x, self.y))


#List#############################################
fly = None
frog = Frog()
#Game Loop########################################
while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            frog.tonguePoke()
    pressedKeys = pygame.key.get_pressed()
    # 시작 화면
    if menu == "start":
        screen.fill((255, 255, 255))
        screen.blit(startScreenImg, (300, 100))
        txt = font1.render("Play", True, (255, 255, 255))
        txtX = 705
        txtY = 435
        buttonRect = pygame.Rect((txtX, txtY), txt.get_size())
        pygame.draw.rect(screen, (200, 50, 0), buttonRect)
        screen.blit(txt, (txtX, txtY))
        # 버튼 위치에서 마우스 왼쪽 클릭시 menu 게임화면으로 변경
        if pygame.mouse.get_pressed()[0] and buttonRect.collidepoint(pygame.mouse.get_pos()):
            menu = "game"
            gameStart = time.time()  # 게임 시작시간 저장
    # 게임 화면
    if menu == "game":
        # 게임시작시, 파리 생성 4.4초 뒤, 파리가 개구리에 먹혔을 때 새 파리 생성
        if fly == None or (time.time() > fly.spawnTime + 4.4 and not fly.stuck):
            fly = Fly()
        if fly.stuck and frog.tongueDist <= 0:  # 파리를 잡고 혀 길이가 0 이하일 때
            frog.energy = min(100, frog.energy + 50)  # 개구리 에너지 증가(100 이하로 유지)
            fly = Fly()

        screen.fill((255, 255, 255))

        frog.move()
        frog.draw()
        fly.stick()
        fly.draw()

        frog.energy -= 0.1  # 개구리 에너지 줄이기
        # 개구리 에너지 바 그리기
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 20, 100))
        if frog.energy >= 0:
            pygame.draw.rect(screen, (200, 50, 0), (10, 110, 20, -frog.energy))
        # 개구리 에니지가 0이하고 이미 죽은 상태가 아니고 혀길이가 0이하면 사망시간 기록
        # deathTime은 0이 아니므로 참 값을 갖고 있다.
        if frog.energy <= 0 and not deathTime and frog.tongueDist <= 0:
            deathTime = time.time()
        if deathTime:  # 죽었으면 생존시간 표시
            txt = font2.render("Survival Time: "+str(int((deathTime-gameStart)*10)/10.),
                               True, (0, 0, 0), screen.blit(txt, (screen.get_width()/2-txt.get_width()/2, 10)))
        else:  # 생존 동안
            # 생존시간 계산해 표시(10을 곱해 정수로 바꾸고 다시 10.0으로 나눠 한자리 수 실수로 표시)
            txt = font2.render("Survival Time: "+str(int((time.time()-gameStart)*10)/10.),
                               True, (0, 0, 0), screen.blit(txt, (screen.get_width()/2-txt.get_width()/2, 10)))
        # 죽은 상태고 2초가 경과해 개구리 이미지가 완전히 사라지면
        if deathTime and time.time() > deathTime + 2:
            menu = "dead"
    # 게임오버 화면
    if menu == "dead":
        screen.fill((255, 255, 255))
        screen.blit(gameoverImg, (300, 100))
        txt = font2.render("You Survived: "+str(int((deathTime-gameStart)*10)/10.)
                           + "seconds", True, (0, 0, 0))
        screen.blit(txt, (705, 500))
        txt = font1.render("Play", True, (255, 255, 255))
        txtX = 705
        txtY = 435
        buttonRect = pygame.Rect((txtX, txtY), txt.get_size())
        pygame.draw.rect(screen, (200, 50, 0), buttonRect)
        screen.blit(txt, (txtX, txtY))
        # 버튼 위치에서 마우스 왼쪽 클릭시 menu 게임화면으로 변경
        if pygame.mouse.get_pressed()[0] and buttonRect.collidepoint(pygame.mouse.get_pos()):
            # 게임 변수들 재설정
            menu = "game"
            gameStart = time.time()
            energy = 100
            deathTime = False
            fly = None
            frog = Frog()

    pygame.display.update()
