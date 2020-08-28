# 2인용 탱크 게임
# 게임은 시작화면/게임화면/게임오버화면으로 구성
# 각자 키보드로 자신의 탱크를 조작
# 포탄 발사하면 포탄은 벽에 최대 5번 튕기며 이동
# 포탄과 벽에 충돌시 탱크의 생명력 감소
# 생명력 3개가 모두 소진되면 상대의 승리
# 탄약고 획득시 포탄 수 증가
# 각 이미지 크기: 탱크들(62*81),벽(200*15),시작화면/적청 승리화면(500*400),배경(1000*600),
# 적청 생명표시(30*30), 잔탄(10*20), 탄약고(44*43)
#Setup###############################################
import pygame
import sys
import math
import random
import time
from pygame.locals import *
# 포탄발사 조금 뒤 소리 재생되는 걸 막기위함
pygame.mixer.init(buffer=512)
pygame.init()
pygame.display.set_caption("Tank Battle")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))

menu = "start"

wallImg = pygame.image.load("images/TBwall.png").convert_alpha()
wallVertImg = pygame.transform.rotate(wallImg, 90)
tankRimg = pygame.image.load("images/TBtankR.png").convert_alpha()
tankBimg = pygame.image.load("images/TBtankB.png").convert_alpha()

startImg = pygame.image.load("images/TBstart.png").convert_alpha()
bgImg = pygame.image.load("images/TBbg.png").convert()
RwinImg = pygame.image.load("images/TBrWin.png").convert_alpha()
BwinImg = pygame.image.load("images/TBbWin.png").convert_alpha()
shellImg = pygame.image.load("images/TBshell.png").convert_alpha()
ammoBoxImg = pygame.image.load("images/TBammo.png").convert_alpha()
Rlives = (
    pygame.image.load("images/TBliveR1.png").convert_alpha(),
    pygame.image.load("images/TBliveR2.png").convert_alpha(),
    pygame.image.load("images/TBliveR3.png").convert_alpha(),
)
Blives = (
    pygame.image.load("images/TBliveB1.png").convert_alpha(),
    pygame.image.load("images/TBliveB2.png").convert_alpha(),
    pygame.image.load("images/TBliveB3.png").convert_alpha(),
)

shellSnd = pygame.mixer.Sound("sounds/shell.ogg")
harmSnd = pygame.mixer.Sound("sounds/tank_hit.ogg")
#Class#################################################


class Tank():
    def __init__(self, x, y, dir, ctrls, img):
        self.x = x
        self.y = y
        self.dir = dir
        self.ctrls = ctrls
        self.img = img
        self.flashTimeEnd = 0
        self.ammo = 5
        self.lives = 3

    # 이동처리
    def move(self):
        dx = math.sin(math.radians(self.dir))
        dy = math.cos(math.radians(self.dir))
        if pressedKeys[self.ctrls[0]]:
            self.x -= dx
            self.y -= dy
        if pressedKeys[self.ctrls[1]]:
            self.x += dx*0.5
            self.y += dy*0.5
        if pressedKeys[self.ctrls[2]]:
            self.dir += 1
        if pressedKeys[self.ctrls[3]]:
            self.dir -= 1
        # 화면 밖으로 나가는 것 방지
        if self.x < -30:
            self.x = -30
        if self.x > 970:
            self.x = 970
        if self.y < -30:
            self.y = -30
        if self.y > 570:
            self.y = 570

    # 총알 생성
    def fire(self):
        if self.ammo > 0:
            # 탱크의 중심좌표, 탱크 향하는 방향을 인자로 주어 새 포탄 생성
            shells.append(Shell(self.x+self.img.get_width()/2,
                                self.y+self.img.get_height()/2, self.dir))
            self.ammo -= 1

    # 총알과의 충돌여부 체크
    def hitShell(self, shell):
        # y에 10을 더한 이유는 회전시를 고려한 것
        # 탱크 안의 가상 직사각형을 좀 작게 만들고 위치를 아래로 좀 이동 시켰다
        return pygame.Rect(self.x, self.y+10, 60, 60).collidepoint(shell.x, shell.y)

    # 벽과의 충돌여부 체크
    def hitWall(self, wall):
        return((wall.vert and
                pygame.Rect((wall.x, wall.y),
                            wallVertImg.get_size()).colliderect((self.x, self.y+10), (60, 60)))
               or (not wall.vert and
                   pygame.Rect((wall.x, wall.y),
                               wallImg.get_size()).colliderect((self.x, self.y+10), (60, 60))))

    # 총알에 맞았을 때 처리
    def harm(self):
        # 2초간은 또 다른 총탄에 맞아도 괜찮게 처리
        if time.time() > self.flashTimeEnd:
            self.flashTimeEnd = time.time() + 2
            self.lives -= 1

    def draw(self):
        # 탱크가 총알에 맞은 상태일 경우 번쩍이게 처리
        # time.time()%0.1은 0~0.1사이 값이 나오는데 그중 0.05이하면 그리지 않으니
        # 1초에 60번 탱크가 나타났다 사라졌다를 반복하는 듯 표현된다
        if time.time() > self.flashTimeEnd or time.time() % 0.1 < 0.05:
            rotated = pygame.transform.rotate(self.img, self.dir)
            screen.blit(rotated, (self.x+self.img.get_width()/2-rotated.get_width()/2,
                                  self.y+self.img.get_height()/2-rotated.get_height()/2))


class Shell:
    # x,y는 탱크 중심 좌표, dir는 탱크가 향하는 방향
    def __init__(self, x, y, dir):
        self.dx = -math.sin(math.radians(dir))*5  # 5는 이동속도
        self.dy = -math.cos(math.radians(dir))*5
        # 포탄을 탱크 향하는 방향 앞쪽에 생성해 포탄과 탱크의 충돌방지
        # 포탄 초기좌표에 초기 방향을 8번 곱한 값을 더하면 탱크 중심에서 40픽셀 떨어진 곳에 포탄 생성
        self.x = x + self.dx * 8
        self.y = y + self.dy * 8
        self.bounces = 0
        shellSnd.play()  # 총알 발사 효과음 내기

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        for wall in walls:
            if wall.vert and pygame.Rect((wall.x, wall.y),
                                         wallVertImg.get_size()).collidepoint(self.x, self.y):
                self.dx *= -1
                self.bounces += 1
            if not wall.vert and pygame.Rect((wall.x, wall.y),
                                             wallImg.get_size()).collidepoint(self.x, self.y):
                self.dy *= -1
                self.bounces += 1
        if self.x < 0 or self.x > 1000:
            self.dx *= -1
            self.bounces += 1
        if self.y < 0 or self.y > 600:
            self.dy *= -1
            self.bounces += 1

    def draw(self):
        pygame.draw.circle(screen, (100, 50, 50),
                           (int(self.x), int(self.y)), 3)


class Ammobox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reappear = 0  # 재생 대기 시간
    # 탱크와의 충돌여부 체크

    def collect(self, tank):
        # 재생 대기 시간이 지났고 탱크와 충돌한 경우
        if (time.time() > self.reappear and
                pygame.Rect((self.x, self.y), ammoBoxImg.get_size())
                .colliderect((tank.x, tank.y+10), (60, 60))):
            # 충돌한 탱크의 탄약 5를 늘린다. (최대치는 10)
            tank.ammo = min(tank.ammo+5, 10)
            # 재생 대기 시간 재설정
            self.reappear = time.time() + 10
            # 생성위치 변경
            if self.y == 20:
                self.y = 500
            else:
                self.y = 20

    def draw(self):
        # 재생 대기 시간을 지났을 경우만 표시
        if time.time() > self.reappear:
            screen.blit(ammoBoxImg, (self.x, self.y))


class Wall():
    def __init__(self, x, y, vert):
        self.x = x
        self.y = y
        self.vert = vert
        self.speed = 1

    def move(self):
        if self.vert:
            self.y += self.speed
        else:
            self.x += self.speed
        if((self.vert and (self.y < 50 or self.y > 350)) or
            (not self.vert and ((self.x < 50 or self.x > 750) or
                                (self.x > 200 and self.x < 600)))):
            self.speed *= -1

    def draw(self):
        if self.vert:
            screen.blit(wallVertImg, (self.x, self.y))
        else:
            screen.blit(wallImg, (self.x, self.y))


#List##################################################
tankR = Tank(740, 20, 180, (K_UP, K_DOWN, K_LEFT, K_RIGHT), tankRimg)
tankB = Tank(200, 500, 0, (K_w, K_s, K_a, K_d), tankBimg)
walls = (Wall(496, 200, True), Wall(50, 150, False),
         Wall(600, 150, False), Wall(50, 435, False), Wall(600, 435, False))
shells = []
ammoboxes = (Ammobox(740, 500), Ammobox(200, 20))
#Game Loop#############################################
while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        # 탱크들 총알 발사 입력 처리
        if event.type == KEYDOWN and event.key == K_RSHIFT and menu == "game":
            tankR.fire()
        if event.type == KEYDOWN and event.key == K_q and menu == "game":
            tankB.fire()
    pressedKeys = pygame.key.get_pressed()
    # 게임 타이틀 모드
    if menu == "start":
        screen.fill((255, 255, 255))
        screen.blit(startImg, (250, 100))
        buttonRect = pygame.Rect(459, 400, 147, 147)
        #pygame.draw.rect(screen, (255, 90, 90), (459, 400, 147, 147))
        if pygame.mouse.get_pressed()[0] and buttonRect.collidepoint(pygame.mouse.get_pos()):
            menu = "game"
    # 게임 실행 모드
    if menu == "game":
        screen.blit(bgImg, (0, 0))
        tankR.move()
        tankB.move()
        tankR.draw()
        tankB.draw()
        # 움직이는 벽들 처리
        for wall in walls:
            wall.move()
            wall.draw()
            # 탱크가 벽에 닿으면 데미지
            if tankR.hitWall(wall):
                tankR.harm()
                harmSnd.play()
            if tankB.hitWall(wall):
                tankB.harm()
                harmSnd.play()
        # 탄약박스 처리
        for ammobox in ammoboxes:
            ammobox.draw()
            ammobox.collect(tankR)
            ammobox.collect(tankB)
        # 총알들 처리
        i = 0
        while i < len(shells):
            shells[i].move()
            shells[i].bounce()
            shells[i].draw()

            flag = False
            # 포탄이 탱크와 충돌하거나 5번 이상 튕기면 제거
            if tankR.hitShell(shells[i]):
                tankR.harm()
                harmSnd.play()  # 효과음 내기
                flag = True
            if tankB.hitShell(shells[i]):
                tankB.harm()
                harmSnd.play()
                flag = True
            if shells[i].bounces >= 5:
                flag = True
            if flag:
                del shells[i]
                i -= 1
            i += 1
        # 남은 생명 이미지 표시
        screen.blit(Rlives[tankR.lives-1], (965, 30))
        screen.blit(Blives[tankB.lives-1], (5, 30))
        # 남은 탄약수 이미지 표시
        for i in range(tankR.ammo):
            screen.blit(shellImg, (987 - i*10, 5))
        for i in range(tankB.ammo):
            screen.blit(shellImg, (5 + i*10, 5))

        # 남은 탱크 수 확인해 게임오버 여부 체크
        if tankR.lives == 0:
            screen.fill((255, 255, 255))
            screen.blit(BwinImg, (250, 100))
            menu = "dead"
        if tankB.lives == 0:
            screen.fill((255, 255, 255))
            screen.blit(RwinImg, (250, 100))
            menu = "dead"
    # 게임오버 모드
    if menu == "dead":
        # 재시작 버튼 클릭시 변수 재설정하고 다시 게임모드로 전환
        #pygame.draw.rect(screen, (255, 90, 90), (575, 380, 333, 88))
        if (pygame.mouse.get_pressed()[0]
                and pygame.Rect((575, 380), (333, 88)).collidepoint(pygame.mouse.get_pos())):
            shells = []
            tankR = Tank(740, 20, 180, (K_UP, K_DOWN,
                                        K_LEFT, K_RIGHT), tankRimg)
            tankB = Tank(200, 500, 0, (K_w, K_s, K_a, K_d), tankBimg)
            ammoboxes = (Ammobox(740, 500), Ammobox(200, 20))
            menu = "game"

    pygame.display.update()
