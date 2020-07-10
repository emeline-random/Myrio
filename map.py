import pygame

import utils
from level import Level
from level_1 import Level1
import images
import constants
import sprites
from level_2 import Level2

MENU_PLATFORMS = pygame.image.load(constants.PATH + "Menu.png")


class Map(Level):

    def __init__(self, player):
        super().__init__(player)
        self.background = pygame.image.load(constants.PATH + "background_menu.png").convert()
        self.max_frames = 1

        menu_levels = [sprites.LevelRound(141, 440, Level1(self.player)),
                       sprites.LevelRound(847, 440, Level2(self.player), 300)]

        platforms = sprites.Platform(MENU_PLATFORMS, 0, 0)
        platforms.player = self.player
        self.platform_list.add(platforms)

        wall = sprites.ClimbingWall(1435, 200, images.PYRANA_PLANT)
        self.wall_list.add(wall)

        for level in menu_levels:
            self.reward_list.add(level)

    def draw(self, screen):
        screen.fill(constants.WHITE)
        screen.blit(self.background, (0, 0))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.reward_list.draw(screen)
        self.block_list.draw(screen)
        self.wall_list.draw(screen)

    def shift_world(self, shift_x):
        self.player.rect.x += shift_x

    def load_sound(self):
        utils.change_sound(constants.PATH + 'menu_sound.mp3')
