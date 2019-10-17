import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(settings,screen,ship,bullets):
    """ 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def check_keydown_events(event,settings,screen,ship,bullets):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key==pygame.K_SPACE:
        fire_bullet(settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key == pygame.K_LEFT:
        ship.moving_left=False


def check_fleet_edges(settings, aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break
def change_fleet_direction(settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def update_aliens(settings,stats,screen,ship, aliens,bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(settings,stats,screen,ship, aliens,bullets)

    #  检查是否有外星人到达屏幕底端
    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)


def update_screen(settings,screen,ship,aliens,bullets):
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    #alien.blitme()
    aliens.draw(screen)
    pygame.display.flip()

def update_bullets(settings,screen,ship,bullets,aliens):
    """ 更新子弹的位置，并删除已消失的子弹 """
    #  更新子弹的位置
    bullets.update()
    #  删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(settings,screen,ship,bullets,aliens)
    

def check_bullet_alien_collisions(settings,screen,ship,bullets,aliens):
    #射杀外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)

    if(len(aliens)==0):
        #  删除现有的所有子弹，并创建一个新的外星人群
        bullets.empty()
        create_fleet(settings,screen,ship,aliens)


def fire_bullet(settings,screen,ship,bullets):
    if len(bullets)< settings.bullets_allowed:
            new_bullet=Bullet(settings,screen,ship)
            bullets.add(new_bullet)


def create_fleet(settings,screen,ship,aliens):
    """ 创建外星人群 """
    #  创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(settings, screen)
    number_aliens_x = 3 #get_number_aliens_x(settings, alien.rect.width)
    number_rows = 2 #get_number_rows(settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number,row_number)

def get_number_aliens_x(settings, alien_width):
    """ 计算每行可容纳多少个外星人 """
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(settings,ship_height, alien_height):
    """ 计算每行可容纳多少行外星人 """
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(settings, screen, aliens, alien_number,row_number):
    """ 创建一个外星人并将其放在当前行 """
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def ship_hit(settings,stats,screen,ship,aliens,bullets):
    if stats.ships_left>0:
        #  将 ships_left 减 1
        stats.ships_left -= 1
        #  清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #  创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        #  暂停
        sleep(0.5)
    else:
        stats.game_active=False


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets):
    """ 检查是否有外星人到达了屏幕底端 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #  像飞船被撞到一样进行处理
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break