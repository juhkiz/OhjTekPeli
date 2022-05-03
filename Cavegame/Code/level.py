from settings import *
from Tiles import StaticTile
import pygame
from support import *
from player import Player
from ui import UI

class Level: 
    def __init__(self, level_data, surface):

        self.display_surface = surface
        self.world_shift = 0

        self.coins = 0

        self.ui = UI(surface)

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprite = self.create_tile_group(coin_layout, 'coins')

    def create_tile_group(self, layout, type):
        sprite_gourp = pygame.sprite.Group()

        for row_index, row in enumerate (layout): #enumerate kertoo millä indeksillä ollaan (millä rivillä)
            for col_index, val in enumerate(row): #for loop käy läpi jokaisen rivin (row:n) merkin ja siitä otetaan indeksi
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./Levels/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'coins':
                        coin_tile_list = import_cut_graphics('./Levels/coin_tiles.png')
                        tile_surface = coin_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    sprite_gourp.add(sprite)

        return sprite_gourp

    def player_setup(self, layout):
         for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)
                if cell == '1':
                    hat_surface = pygame.image.load('./Levels/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.player_movement_speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect): # colliderect function tells us if we collide with our blocks in the map
                if player.direction.x < 0: # if player collides and direction is left then the player is colliding on the right side of the block
                    player.rect.left = sprite.rect.right #stops player at the right spot after collision with the block
                elif player.direction.x > 0:
                    player.rect.right  =sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect): # colliderect function tells us if we collide with our blocks in the map
                if player.direction.y > 0: # if player collides and direction is down then the player is colliding on the top side of the block
                    player.rect.bottom = sprite.rect.top #stops player at the right spot after collision with the block
                    player.direction.y = 0 # cancels gravity
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def scroll_x(self):
            player = self.player.sprite
            player_x = player.rect.centerx # gets players x position on the level
            direction_x = player.direction.x # gets players direction on x axis

            if player_x < screen_width / 4 and direction_x < 0: # if player reaches the left side of the map, the camera will shift to left
                self.world_shift = 8 #change camerashift same as player speed 
                player.player_movement_speed = 0 #change playerspeed to 0 (we scroll the map "behinde the player so it seems like the player is moving")
            elif player_x > screen_width - (screen_width / 4) and direction_x > 0: # if player reaches the right side of the map, the camera will shift to right
                self.world_shift = -8
                player.player_movement_speed = 0
            else:
                self.world_shift = 0
                player.player_movement_speed = 8

    def change_coins(self, amount):
        self.coins += amount
    
    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprite, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)
    
    def check_goal_collisions(self):
        goal_collided = pygame.sprite.spritecollide(self.player.sprite, self.goal, True)
        if goal_collided:
            print("Maali!")

    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        self.coin_sprite.update(self.world_shift)
        self.coin_sprite.draw(self.display_surface)

        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.ui.show_coins(self.coins)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_goal_collisions()

        self.check_coin_collisions()