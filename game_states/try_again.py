import pygame
from utils.configs import WINDOW_HEIGHT, WINDOW_WIDTH


def try_again(win, font, font_small):
    respawn_start = pygame.time.get_ticks()
    explosion_alpha = 0
    seconds = 0
    while seconds <= 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        # fade to white (explosion)
        if explosion_alpha < 200:
            explosion_alpha += 5

        explosion = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.SRCALPHA, 32)
        explosion = explosion.convert_alpha()
        explosion.fill((255, 255, 255, explosion_alpha))
        win.blit(explosion, (0, 0))

        lost_text = font.render("Você perdeu!", True, (255, 0, 0))
        win.blit(
            lost_text,
            (
                WINDOW_WIDTH / 2 - lost_text.get_width() / 2,
                WINDOW_HEIGHT / 2 - lost_text.get_height() / 2,
            ),
        )

        seconds = int((pygame.time.get_ticks() - respawn_start) / 1000)
        if seconds <= 5:
            try_again = font_small.render(
                "Tente novamente em {} segundos".format(5 - seconds), True, (0, 0, 0)
            )
        win.blit(
            try_again,
            (
                WINDOW_WIDTH / 2 - try_again.get_width() / 2,
                WINDOW_HEIGHT / 2 - try_again.get_height() / 2 + 100,
            ),
        )

        pygame.display.flip()
