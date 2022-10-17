import pygame
import cv2
from game_states.try_again import try_again
from models.Knife import Knife
from utils.add_bombs import add_bombs
from utils.collision_handler import collision_handler
from utils.configs import (
    BACKGROUND_PATH,
    FPS,
    IMG_PATH,
    WINDOW_HEIGHT,
    WINDOW_SIZE,
    WINDOW_WIDTH,
)
from utils.fruits_behavior import fruits_behavior
from utils.throw_fruits import throw_fruits

# Import do Mediapipe
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pygame.display.set_icon(pygame.image.load(IMG_PATH + "icon.png"))
pygame.display.set_caption("Fruit Ninja With Mediapipe Hands!")


def game_loop():

    # INITIAL SETTINGS AND LOADING FONTS
    pygame.init()
    font = pygame.font.Font("./font/go3v2.ttf", 100)
    font_small = pygame.font.Font("./font/go3v2.ttf", 50)

    # GET VIDEO CAPTURE FROM WEBCAM
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)

    # GAME VARIABLES
    run = True
    exploding = False

    # GAME WINDOW
    win = pygame.display.set_mode(WINDOW_SIZE)

    # BACKGROUND IMAGE
    background = pygame.image.load(BACKGROUND_PATH)
    background_cv2 = cv2.imread(BACKGROUND_PATH)

    # GLOBAL VARIABLES FOR GAME OBJECTS
    knf = Knife(win)
    fruits = []

    # Main loop
    while run:
        # NEW ROUND
        if not exploding:
            # CREATE BOMBS AND FRUITS
            throw_fruits(fruits, win)
            add_bombs(fruits, win)

            # ROUND START
            while fruits != [] and run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        knf.enable_cutting()

                    elif event.type == pygame.MOUSEBUTTONUP:
                        knf.disable_cutting()

                pygame.time.delay(FPS)

                # DISPLAY BACKGROUND IMAGE
                win.blit(
                    pygame.transform.scale(
                        background, (WINDOW_WIDTH, WINDOW_HEIGHT)
                    ),
                    (0, 0),
                )

                # UPDATE KNIFE POSITION
                knf.update(pygame.mouse.get_pos())

                # CHECK FOR KNIFE COLLISIONS AND UPDATE FRUITS
                state = fruits_behavior(knf, fruits)
                if state == "explode":
                    exploding = True
                    break

                pygame.display.flip()
        # GAME OVER STATE
        else:
            try_again(win, font, font_small)
            exploding = False
            fruits = []

        if not run:
            pygame.quit()
            break


if __name__ == "__main__":
    game_loop()
