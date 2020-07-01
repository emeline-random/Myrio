import constants
import images
import sprites
import level
import pygame


class MyLevel(level.Level):
    def __init__(self, player):
        level.Level.__init__(self, player)

        self.background = pygame.image.load("data/background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 2
        self.number = 0

        # Array with type of platform, and x, y location of the platform.
        platform = [sprites.Platform(images.get_platform(images.GROUND, 429), 0, 480),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 92, images.COLUMN_C), 415, 458),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 129, images.COLUMN_C), 455, 421),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 165, images.COLUMN_C), 493, 385),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 199, images.COLUMN_C), 530, 351),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 234, images.COLUMN_C), 568, 316),
                    sprites.Platform(images.get_platform(images.GROUND, 384, 235, images.GROUND_C), 606, 316),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 145, images.COLUMN_C, images.COLUMN_B),
                                     1067, 265),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 145, images.COLUMN_C, images.COLUMN_B),
                                     1207, 210),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 145, images.COLUMN_C, images.COLUMN_B),
                                     1408, 251),
                    sprites.Platform(images.get_platform(images.GROUND, 440), 1602, 226),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 145, images.COLUMN_C, images.COLUMN_B),
                                     2034, 226),
                    sprites.Platform(images.get_platform(images.PLATFORM, 180), 1945, 507),
                    sprites.Platform(images.get_platform(images.GROUND, 438), 2252, 383),
                    sprites.Platform(images.get_platform(images.GROUND, 869), 2685, 439),
                    sprites.Platform(images.get_platform(images.COLUMN, 46, 492, images.COLUMN_C, images.COLUMN_B),
                                     3543, 319),
                    sprites.HorizontalMovingPlatform(images.get_platform(images.GROUND, 145, 32), 3655, 324, 4011,
                                                     3650),
                    sprites.VerticalMovingPlatform(images.get_platform(images.GROUND, 145, 32), 4207, 400, 100, 500),
                    sprites.Platform(images.get_platform(images.GROUND, 433), 4464, 134),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C), 4985,
                                                   300, 150, 427),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_R, 90, 440, images.PIPE_R_C), 5075,
                                                   350, 200, 400),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C), 5165,
                                                   250, 170, 380),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C), 5255,
                                                   400, 220, 427),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C), 5345,
                                                   300, 180, 380),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C), 5700,
                                                   270, 160, 420),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_R, 90, 440, images.PIPE_R_C), 5790,
                                                   350, 220, 400),
                    sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C), 5975,
                                                   300, 200, 390),
                    sprites.Platform(images.get_platform(images.GROUND, 145), 6214, 359),
                    sprites.Platform(images.get_platform(images.GROUND, 300, 550, images.GROUND_C), 6359, 0)]
        level_pipes = [sprites.Pipe(self, 2750, 1776),
                       sprites.Pipe(level.Level02(self.player), 0, 2845, 0),
                       sprites.Pipe(level.Level02(self.player), 0, 5880, 339,
                                    images.get_platform(images.PIPE_B, 95, 215, images.PIPE_B_C))]
        level_blocks = [sprites.BreakableBlock(710, 135),
                        sprites.BreakableBlock(802, 135),
                        sprites.BreakableBlock(1877, 48),
                        sprites.Block(None, 2846, 396),
                        sprites.Block(None, 2892, 396),
                        sprites.QBlock(756, 135, sprites.Reward(None)),
                        sprites.QBlock(1923, 48, sprites.Piece(1923, 48))]
        level_enemies = [sprites.GoombaEnemy(831, 270),
                         sprites.KoopaEnemy(3002, 358),
                         sprites.KoopaEnemy(3400, 358)]

        # Go through the arrays above and add platforms
        for platform in platform:
            platform.player = self.player
            self.platform_list.add(platform)

        for pipe in level_pipes:
            pipe.level = self
            pipe.player = self.player
            self.platform_list.add(pipe)

        for aBlock in level_blocks:
            self.block_list.add(aBlock)
            if isinstance(aBlock, sprites.BreakableBlock):
                aBlock.level = self

        for enemy in level_enemies:
            enemy.player = self.player
            self.enemy_list.add(enemy)

        self.add_flag(level.Level02(self.player))