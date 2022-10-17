import math
import random

import pygame

from utils.configs import WINDOW_HEIGHT, WINDOW_WIDTH, IMG_PATH


class Fruit:
    def __init__(self, name, win, cut=False):
        self.name = name
        # print(self.name)
        self.image = pygame.image.load(IMG_PATH + name + ".png")
        self.rect = self.image.get_rect()
        self.width, self.height = self.image.get_size()

        self.cut = cut
        self.pos = [
            random.randint(self.width, WINDOW_WIDTH - self.width),
            WINDOW_HEIGHT + (self.height + 1) // 2,
        ]

        self.update_rect()

        self.win = win
        self.destroy = False

        # physics configuration ---------------------------
        self.time = 0
        self.time_step = random.uniform(0.15, 0.2)
        self.spos = [self.pos[0], self.pos[1]]

        if self.pos[0] > (WINDOW_WIDTH // 2):
            self.s_angle = random.uniform(math.pi / 2, math.pi / 2 + math.pi / 18)
        else:
            self.s_angle = random.uniform(4 * math.pi / 9, math.pi / 2)

        self.speed = random.randint(
            int(0.14 * WINDOW_HEIGHT), int(0.16 * WINDOW_HEIGHT)
        )
        self.svelx = self.speed * math.cos(self.s_angle)
        self.svely = -self.speed * math.sin(self.s_angle)

        self.time_limit = (
            -self.svely + math.sqrt(self.svely**2 + 16 * self.spos[1])
        ) / 8
        self.angle = 0
        if self.svelx > 0:
            self.angle_speed = -5
        else:
            self.angle_speed = 5

    def stop(self, angle=0):
        self.spos = [self.pos[0], self.pos[1]]
        self.time = 0
        self.s_angle = angle
        self.angle_speed = 1

        # --------------------------------------------------

    def change_image(self, name):
        self.image = pygame.image.load(IMG_PATH + name + ".png")

    def change_xspeed(self, speed):
        self.svelx = speed

    def change_yspeed(self, speed):
        self.svely = speed

    def change_rot_speed(self, speed):
        self.angle_speed = speed

    def rotate(self, angle):
        self.angle = angle

    def update_rect(self):
        self.rect.top = self.pos[1]
        self.rect.bottom = self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width

    def draw(self):
        rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        rotFruit = rotatedSurf.get_rect()
        rotFruit.center = tuple(self.pos)
        self.win.blit(rotatedSurf, rotFruit)

    def physic(self):

        gravity = 5

        if self.time <= self.time_limit:
            self.time += self.time_step
            self.pos[0] = self.spos[0] + self.svelx * (self.time)
            self.pos[1] = (
                self.spos[1] + self.svely * (self.time) + (gravity * (self.time**2))
            )

        else:
            self.destroy = True

    def update(self):

        self.angle = (self.angle + self.angle_speed) % 360
        self.physic()
        self.update_rect()
        self.draw()

    # private

    def copy(self):
        newfr = Fruit(self.name, self.win, self.cut)
        newfr.pos = self.pos
        newfr.update_rect()

        # physics configuration ---------------------------
        newfr.time = self.time
        newfr.time_step = self.time_step
        newfr.spos = self.spos

        newfr.s_angle = self.s_angle

        newfr.speed = self.speed
        newfr.svelx = self.svelx
        newfr.svely = self.svely
        newfr.angle = self.angle
        return newfr
