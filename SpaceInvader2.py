# 위에서 떨어져 내리는 적과 주인공 충돌시 게임 오버
# 좌우 화살표키로 주인공 좌우 이동, 스페이스 클릭시 총알 발사
# 적과 총알 충돌시 적 제거
# 사용한 적 그림 크기: 70*45, 주인공 그림 크기: 100*59
# Setup==========================================
import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((640, 650))
clock = pygame.time.Clock()
lastEnemySpawnTime = 0 #마지막 적 생성 시간
score = 0 # 점수
font = pygame.font.Font(None, 20) #기본폰트, 크기 20
#사용가능한 폰트는 Python Shell에서 import pygame한 뒤 pygame.font.get_fonts()로 볼 수 있단다.
shots = 0 #미사일 발사횟수
hits = 0 #맞힌 적 수
misses = 0 #놓친 적 수

playerImg = pygame.image.load("images/pygameFighter1.png").convert_alpha()
#playerImg.set_colorkey((255,255,255)) #하얀색을 투명으로
enemyImg = pygame.image.load("images/pygameEnemy1.png").convert_alpha()
overImg = pygame.image.load("images/pygameOver.png").convert_alpha()
#Class==========================================
class Player: # 주인공 관련
    def __init__(self): #초기화
        self.x = 320
    def move(self): #이동 관련
        if pressedKeys[K_LEFT] and self.x > 0:
            self.x -= 3
        if pressedKeys[K_RIGHT] and self.x < 540:
            self.x += 3  
    def fire(self): #미사일 리스트에 새 미사일 추가
        global shots #미사일 발사수 
        shots += 1
        missiles.append(Missile(self.x + 50))
    def hitBy(self, enemy): #주인공과 적 충돌 체크
        return(
            enemy.y > 585 and
            enemy.x > self.x - 55 and
            enemy.x < self.x + 85
        )
    def draw(self): #화면에 그리기
        screen.blit(playerImg, (self.x, 591))

class Missile:
    def __init__(self, x):
        self.x = x
        self.y = 591
    def move(self):
        self.y -= 5
    #미사일이 화면 위로 나갔는지 체크
    def offScreen(self): 
        return self.y < -8
    def draw(self):
        #직선 그리기(그릴 곳, 색, 시작점, 끝점, 두께)
        pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x, self.y + 8), 5)

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
    #적과 미사일의 충돌여부 체크(직사각형의 경우)
    def touchingRect(self, missile):
        return pygame.Rect((self.x, self.y), (70,45)).collidepoint(missile.x, missile.y)
    #적과 미사일의 충돌여부 체크(적을 원으로 생각할 경우)
    def touchingCircle(self, missile):
        #적의 중심인 35, 22로 미사일 위치와의 차이를 비교하여 대각선 길이가 1225(35의 제곱)보다 작으면 충돌
        return (self.x + 35 - missile.x)**2 + (self.y + 22 - missile.y)**2 < 1225
    #점수 처리
    def score(self):
        global score
        score += 100
    def draw(self): #화면에 그리기
        screen.blit(enemyImg, (self.x, self.y))
# List==========================================
player = Player()
missiles = []
enemies = []
# Game Loop==========================================
while 1:
    clock.tick(60) #시간 인터벌 설정
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        # 스페이스 클릭시 총알생성 매서드 호출
        if event.type == KEYDOWN and event.key == K_SPACE:
            player.fire()
        #눌린 키보드 정보 받아오기
        pressedKeys = pygame.key.get_pressed()

    # 0.5초 마다 새 적을 리스트에 추가시키기
    if time.time() - lastEnemySpawnTime > 0.5:
        enemies.append(Enemy())
        lastEnemySpawnTime = time.time()

    screen.fill((0,0,0)) #화면 검은색으로 칠하기
    #주인공 처리 관련
    player.move()
    player.draw()
    # 적 처리 관련
    i = 0
    while i < len(enemies):
        enemies[i].move() #적 이동
        enemies[i].bounce() #적 좌우 화면 이탈시 방향 바꾸기
        enemies[i].draw() #적 화면에 그리기
        if enemies[i].offScreen(): #화면 아래로 나간 적 제거하기
            del enemies[i]
            i -= 1
        i += 1
    # 미사일 처리 관련
    i = 0
    while i < len(missiles):
        missiles[i].move()
        missiles[i].draw()
        if missiles[i].offScreen(): #화면 위로 올라가면
            del missiles[i]
            misses += 1 #못 맞힌 수 늘리기
            i -= 1
        i += 1
    #적과 미사일 충돌 처리
    i = 0
    while i < len(enemies):
        j = 0
        while j < len(missiles):
            #if enemies[i].touchingRect(missiles[j]): #직사각형 검사
            if enemies[i].touchingCircle(missiles[j]): #원 검사
                enemies[i].score() #점수 올리는 메서드 호출
                hits += 1 #맞힌 적 수 늘리기
                del enemies[i] #충돌한 적과 미사일 제거
                del missiles[j]
                i -= 1
                break
                #break로 빠져나가기에 j -= 1은 필요없다
            j += 1
        i += 1
    #적과 주인공 충돌 처리
    for enemy in enemies:
        if player.hitBy(enemy):
            screen.blit(overImg, (170,200)) #게임오버 이미지 띄우기
            #여러 정보들 텍스트 띄우기
            screen.blit(font.render("Total Shots: "+str(shots), True, (255,255,255)), (180,320))
            screen.blit(font.render("Score: "+str(score), True, (255,255,255)), (180,370))
            screen.blit(font.render("On Target: "+str(hits), True, (255,255,255)), (350,320))
            screen.blit(font.render("Missed: "+str(misses), True, (255,255,255)), (350,370))
            if shots == 0: #0나눔 에러 방지용
                screen.blit(font.render("Accuracy: --", True,(255,255,255)),(350,420))
            else:
                #정확도 소숫점 아래 1자리만 표시하게 하기
                screen.blit(font.render("Accuracy: "+"{:.1f}%".format(100*hits/shots), 
                                                    True, (255,255,255)), (350,420))
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                pygame.display.update()

    #점수 화면 표시 blit(render(표시할 내용, 안티알리어스 사용여부, 색상), 텍스트 위치)
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (15,15))
    #모든 변화 업데이트
    pygame.display.update() 