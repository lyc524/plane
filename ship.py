import pygame
class Ship():
    def __init__(self,screen):
        self.screen=screen
        #  加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('images/ship.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #  将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right=False
        self.moving_left=False

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image, self.rect)


    def update(self):
        if self.moving_right:
            self.rect.centerx +=1
        if self.moving_left:
            self.rect.centerx -= 1