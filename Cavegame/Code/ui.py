import pygame

class UI: 
    def __init__(self, surface):

        self.display_surface = surface

        self.coin = pygame.image.load('./Levels/uiCoin.png')
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('./Levels/ARCADEPI.TTF', 30)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, 'white')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4 ,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)
