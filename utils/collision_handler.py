import math

from utils.configs import FPS, WINDOW_HEIGHT


def collision_handler(frt):
    # case 1
    # knife_angle = knf.angle
    fruit_angle = frt.angle

    topFruit = frt.copy()
    topFruit.cut = True
    topFruit.change_image(topFruit.name + "-2")

    topFruit.svely = -0.3 * FPS / 20 * abs(topFruit.svely)

    botFruit = frt.copy()
    botFruit.cut = True
    botFruit.change_image(botFruit.name + "-1")

    botFruit.svely = -0.3 * FPS / 20 * abs(botFruit.svely)

    shoot_angle = math.pi / 6
    new_vx = abs((0.08 * WINDOW_HEIGHT) * math.cos(shoot_angle))
    if fruit_angle >= (2 * math.pi - math.pi / 2) and fruit_angle <= math.pi / 2:
        topFruit.stop(shoot_angle)
        topFruit.rotate(2 * math.pi - math.pi / 2)
        botFruit.stop(math.pi - shoot_angle)
        botFruit.rotate(math.pi / 2)

        topFruit.svelx = -new_vx
        botFruit.svelx = new_vx
    else:
        topFruit.stop(math.pi - math.pi / 18)
        topFruit.rotate(2 * math.pi - math.pi / 2)
        botFruit.stop(math.pi / 18)
        botFruit.rotate(math.pi / 2)
        topFruit.svelx = new_vx
        botFruit.svelx = -new_vx

    return topFruit, botFruit
