import pygame

import sprites
import constants
from level import Level
from level import Level02
import images


class Level01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load("data/background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 1
        self.number = 0

        # Array with type of platform, and x, y location of the platform.
        platform = [sprites.Platform(images.get_platform(images.PLATFORM, 320), 213, 367),
                    sprites.Platform(images.get_platform(images.PLATFORM, 160), 1227, 398),
                    sprites.Platform(images.get_platform(images.PLATFORM, 160), 1498, 262),
                    sprites.Platform(images.get_platform(images.PLATFORM, 213), 3306, 346),
                    sprites.Platform(images.get_platform(images.PLATFORM, 160), 4240, 267)]
        level_blocks = [sprites.BreakableBlock(373, 160),
                        sprites.BreakableBlock(2021, 340, images.get_blocks(images.BREAK_BLOCK, 6)),
                        sprites.BreakableBlock(2121, 131),
                        sprites.Block(None, 2507, constants.HEIGHT-50),
                        sprites.BreakableBlock(3253, 367, images.empiled_blocks(images.BREAK_BLOCK, 4)),
                        sprites.Block(images.PIPE_BLOCK, 3733, 209),
                        sprites.BreakableBlock(4848, 314, images.get_blocks(images.BREAK_BLOCK, 5))]
        level_rewards = [sprites.QBlock(4898, 104, sprites.Reward(None)),
                         sprites.QBlock(4948, 104, sprites.Reward(None)),
                         sprites.QBlock(4998, 104, sprites.Reward(None))]
        level_enemies = [sprites.GoombaEnemy(856),
                         sprites.KoopaEnemy(1000),
                         sprites.KoopaEnemy(2720),
                         sprites.KoopaEnemy(2950),
                         sprites.GoombaEnemy(4053)]

        # Go through the arrays above and add platforms
        for platform in platform:
            platform.player = self.player
            self.platform_list.add(platform)

        for aBlock in level_blocks:
            self.block_list.add(aBlock)
            if isinstance(aBlock, sprites.BreakableBlock):
                aBlock.level = self

        for aBlock in level_rewards:
            aBlock.level = self
            aBlock.player = self.player
            self.block_list.add(aBlock)

        for enemy in level_enemies:
            enemy.player = self.player
            self.enemy_list.add(enemy)

        pipe = sprites.Pipe(Level02(self.player), 1520, 3573)
        pipe.player = self.player
        pipe.level = self
        self.platform_list.add(pipe)

        self.add_flag(Level02(self.player))
