import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pygame.math.Vector2(0,0) # vector is a list that contains an x and y value
        self.player_movement_speed = 8
        self.gravity = 0.8
        self.jump_speed = -16



    def get_input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys_pressed[pygame.K_SPACE]:
            self.apply_jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def apply_jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()