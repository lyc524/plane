import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    pygame.init()
    pygame.display.set_caption("lz")

    settings = Settings()
    screen=pygame.display.set_mode((settings.screen_width,settings.screen_height))
    ship=Ship(screen)
    while True:
        gf.check_events(ship)
        gf.update_screen(settings,screen,ship)

run_game()