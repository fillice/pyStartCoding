import pygame
import sys
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
fighterImg = pygame.image.load("images/pygameFighter1.png").convert_alpha()


class Fighter:
    def __init__(self):
        self.x = 450
        self.y = 270
        self.dir = 0

    def turn(self):
        if pressedKeys[K_a]:
            self.dir += 1
        if pressedKeys[K_d]:
            self.dir -= 1

    def draw(self):
        #rotate(회전대상, 회전각도)
        rotated = pygame.transform.rotate(fighterImg, self.dir)
        screen.blit(rotated, (self.x+fighterImg.get_width()/2-rotated.get_width()/2,
                              self.y+fighterImg.get_height()/2-rotated.get_height()/2))


fighter = Fighter()

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pressedKeys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    fighter.draw()
    fighter.turn()

    pygame.display.update()
