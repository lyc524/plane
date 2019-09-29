import sys
import pygame
def check_events(ship):
    """ 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                ship.moving_right=True
            elif event.key==pygame.K_LEFT:
                ship.moving_left=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right=False
            elif event.key == pygame.K_LEFT:
                ship.moving_left=False

def update_screen(settings,screen,ship):
    screen.fill(settings.bg_color)
    ship.blitme()
    pygame.display.flip()