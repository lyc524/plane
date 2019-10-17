import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats

def run_game():
    pygame.init()
    pygame.display.set_caption("lz")



    settings = Settings()
    screen=pygame.display.set_mode((settings.screen_width,settings.screen_height))

    #  创建一个用于存储游戏统计信息的实例
    stats = GameStats(settings)
    
    ship=Ship(settings,screen)
    bullets=Group()
    aliens=Group()

    gf.create_fleet(settings,screen,ship,aliens)

    while True:
        gf.check_events(settings,screen,ship,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings,screen,ship,bullets,aliens)
            gf.update_aliens(settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(settings,screen,ship,aliens,bullets)

run_game()