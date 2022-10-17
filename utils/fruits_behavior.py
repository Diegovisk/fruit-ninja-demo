import pygame

from utils.collision_handler import collision_handler


def fruits_behavior(knf, fruits):
    for fr in fruits:
        fr.update()
        # IF FRUIT IS CUT AND KNIFE IS CUTTING
        if (
            pygame.sprite.collide_rect(knf, fr) == True
            and knf.sharp()
            and not fr.cut
        ):
            if fr.name == "bomb":
                fruits = []
                return "explode"

            top, bot = collision_handler(fr)
            fruits.append(top)
            fruits.append(bot)
            fruits.remove(fr)
            knf.cut()

        if fr.destroy == True:
            fruits.remove(fr)