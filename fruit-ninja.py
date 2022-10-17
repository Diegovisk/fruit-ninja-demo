import numpy as np
import pygame
import math
import random
import sys
import cv2
import mediapipe as mp
from game_states.try_again import try_again
from models.Fruit import Fruit
from models.Knife import Knife
from utils.add_bombs import add_bombs
from utils.coin_flip import coin_flip
from utils.collision_handler import collision_handler
from utils.configs import BACKGROUND_PATH, FPS, FRUIT_LIST, IMG_PATH, WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_WIDTH
from utils.is_pointing_finger import is_pointing_gesture
from utils.throw_fruits import throw_fruits

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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

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
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1,
    ) as hand:

        while cap.isOpened() and run:
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

                    success, frame = cap.read()

                    if not success:
                        continue
                    
                    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                    frame.flags.writeable = False
                    results = hand.process(frame)

                    finger_tip_pixel_coordinates = None

                    # Draw the hand annotations on the image.
                    background_with_hands = background_cv2.copy()
                    if results.multi_hand_landmarks != None:
                        for hand_landmarks in results.multi_hand_landmarks:
                            finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                            finger_tip_pixel_coordinates = mp_drawing._normalized_to_pixel_coordinates(finger_tip.x, finger_tip.y, WINDOW_WIDTH, WINDOW_HEIGHT)
                            
                            print(finger_tip_pixel_coordinates)

                            mp_drawing.draw_landmarks(
                                background_with_hands, hand_landmarks, mp_hands.HAND_CONNECTIONS
                            )

                            if is_pointing_gesture(hand_landmarks):
                                knf.enable_cutting()
                            else:
                                knf.disable_cutting()
                    
                    # Display the image.
                    # image needs to be rotated in pygame
                    background_with_hands = np.rot90(cv2.flip(background_with_hands, 1))
                    
                    # CV2 uses BGR colors and PyGame needs RGB
                    background_with_hands = cv2.cvtColor(background_with_hands, cv2.COLOR_BGR2RGB)
                    background_with_hands = cv2.resize(background_with_hands, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_LINEAR)
                    background_with_hands = pygame.surfarray.make_surface(background_with_hands)

                    pygame.time.delay(FPS)
                    
                    win.blit(pygame.transform.scale(background_with_hands, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

                    if finger_tip_pixel_coordinates != None:
                        knf.update(finger_tip_pixel_coordinates)
                    # knf.update(pygame.mouse.get_pos())

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
                                exploding = True
                                break

                            top, bot = collision_handler(fr)
                            fruits.append(top)
                            fruits.append(bot)
                            fruits.remove(fr)
                            knf.cut()

                        if fr.destroy == True:
                            fruits.remove(fr)

                    pygame.display.flip()
            # Game over
            else:
                try_again(win, font, font_small)
                exploding = False
                fruits = []

            if not run:
                cap.release()
                pygame.quit()
                break


if __name__ == "__main__":
    game_loop()