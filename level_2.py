import constants
import images
import sprites
import level
import pygame
from level_1 import Level1_2

LEVEL02_platforms = pygame.image.load("data/level_2.png")


class Level2(level.Level):
    def __init__(self, player):
        level.Level.__init__(self, player)

        self.background = pygame.image.load("data/background_l2.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 2
        self.number = 0

        platforms = sprites.Platform(LEVEL02_platforms, 0, 0)
        platforms.player = self.player
        self.platform_list.add(platforms)

        pipe = sprites.Pipe(Level1_2(self.player, self), 0, 3880, 415, images.get_platform(
            images.PIPE_R, images.PIPE_R.get_rect().width, 140, images.PIPE_R_C))
        pipe.level = self
        pipe.player = self.player
        self.platform_list.add(pipe)

        level_blocks = [sprites.BreakableBlock(983, 256),
                        sprites.QBlock(1029, 256, sprites.Reward(None)),
                        sprites.QBlock(3222, 12, sprites.Reward(None), True)]
        level_platforms = [sprites.HorizontalMovingPlatform(images.PLATFORM_Y, 1200, 423, 1712, 1140),
                           sprites.HorizontalMovingPlatform(images.PLATFORM_Y, 1400, 292, 1712, 1140)]
        level_enemies = [sprites.Cheep(1154, 214, 1647, 1147),
                         sprites.Cheep(1177, 111, 1670, 1170),
                         sprites.Cheep(1260, 168, 1727, 1227),
                         sprites.Cheep(3409, 216, 3639, 3110),
                         sprites.Cheep(3434, 138, 3664, 3135),
                         sprites.Cheep(3482, 367, 3712, 3183),
                         sprites.Cheep(3507, 290, 3737, 3208),
                         sprites.Cheep(3515, 180, 3745, 3216),
                         sprites.Cheep(3590, 333, 3820, 3291),
                         sprites.Cheep(3654, 233, 3884, 3355),
                         sprites.Cheep(3677, 154, 3907, 3378),
                         sprites.Cheep(3760, 198, 3990, 3461),
                         sprites.Hurchin(2005, 385, 45, 390),
                         sprites.Hurchin(2180, 45, 45, 390),
                         sprites.Hurchin(2750, 55, 45, 265, True)]

        star_coin = sprites.StarCoin(1820, 26, 0)
        self.reward_list.add(star_coin)
        self.star_coins.add(star_coin)

        # # Go through the arrays above and add platforms
        for platform in level_platforms:
            platform.player = self.player
            self.platform_list.add(platform)
        for aBlock in level_blocks:
            self.block_list.add(aBlock)
            if isinstance(aBlock, sprites.BreakableBlock):
                aBlock.level = self
        for enemy in level_enemies:
            enemy.player = self.player
            self.enemy_list.add(enemy)

    def begin(self):
        self.player.set_swim(True)
