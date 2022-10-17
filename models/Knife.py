import math
import pygame

from utils.configs import IMG_PATH


max_tail_size = 5


class Knife:
    def __init__(self, win):
        self.pos = pygame.mouse.get_pos()
        self.drag = True
        self.win = win
        self.tail_size = 0
        self.tail = []
        self.width = 7
        self.height = 7
        self.default_size = (7, 7)
        self.angle = 0
        self.enable_cut = False
        self.image = pygame.Surface(self.default_size)
        self.rect = self.image.get_rect()
        self.rect.top = self.pos[1]
        self.rect.bottom = self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width
        self.flash = pygame.image.load(IMG_PATH + "flash.png")

    def sharp(self):
        return self.enable_cut

    def enable_cutting(self):
        self.enable_cut = True

    def disable_cutting(self):
        self.enable_cut = False

    def draw(self):
        size = 7
        factor = 0.8
        if self.drag:
            for pos in reversed(self.tail):
                pygame.draw.rect(
                    self.win, (255, 255, 255), (pos[0], pos[1], size, size)
                )
                size = factor * size

    def find_angle(self):
        if len(self.tail) > 2:
            try:
                self.angle = math.atan(
                    abs(
                        (self.tail[-1][1] - self.tail[-2][1])
                        / (self.tail[-1][0] - self.tail[-2][0])
                    )
                )
            except:
                self.angle = math.pi / 2

            if (
                self.tail[-1][1] < self.tail[-2][1]
                and self.tail[-1][0] > self.tail[-2][0]
            ):
                self.angle = abs(self.angle)
            elif (
                self.tail[-1][1] < self.tail[-2][1]
                and self.tail[-1][0] < self.tail[-2][1]
            ):
                self.angle = math.pi - self.angle
            elif (
                self.tail[-1][1] > self.tail[-2][1]
                and self.tail[-1][0] < self.tail[-2][0]
            ):
                self.angle = math.pi + abs(self.angle)
            elif (
                self.tail[-1][1] > self.tail[-2][1]
                and self.tail[-1][0] > self.tail[-2][0]
            ):
                self.angle = (math.pi * 2) - self.angle
            else:
                self.angle = 0

    def update_rect(self):
        self.rect.top = self.pos[1]
        self.rect.bottom = self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width

    def update(self, pos):
        self.pos = pos
        self.update_rect()

        if self.tail_size < max_tail_size:
            self.tail.append(self.pos)
            self.tail_size += 1
        else:
            self.tail.pop(0)  # pop firts element
            self.tail.append(self.pos)

        self.find_angle()
        # print(self.angle*180/math.pi)
        self.draw()

    def cut(self, pos=None):
        rotatedFlash = pygame.transform.rotate(self.flash, self.angle * 180 / math.pi)
        rotflash = rotatedFlash.get_rect()
        if pos != None:
            rotflash.center = pos
        else:
            rotflash.center = tuple(self.pos)
        self.win.blit(rotatedFlash, rotflash)
