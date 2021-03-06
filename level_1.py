import pygame
import images
import level
import constants
import sprites
import utils


class Level1(level.Level):
    def __init__(self, player):
        level.Level.__init__(self, player)

        self.background = pygame.image.load(constants.PATH + "background_l1.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 2
        self.number = 0

        platforms = sprites.Platform(pygame.image.load(constants.PATH + "level_1.png"), 0, 0)
        platforms.player = self.player
        self.platform_list.add(platforms)

        # Array with type of platform, and x, y location of the platform.
        level_platforms = [sprites.HorizontalMovingPlatform(images.get_platform(images.GROUND, 145, 32), 3655, 324,
                                                            4011, 3650),
                           sprites.VerticalMovingPlatform(images.get_platform(images.GROUND, 145, 32), 4207, 400, 100,
                                                          500),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C),
                                                          4985, 300, 150, 427),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_R, 90, 440, images.PIPE_R_C),
                                                          5075, 350, 200, 400),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C),
                                                          5165, 250, 170, 380),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C),
                                                          5255, 400, 220, 427),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C),
                                                          5345, 300, 180, 380),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_G, 90, 440, images.PIPE_G_C),
                                                          5700, 270, 160, 420),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_R, 90, 440, images.PIPE_R_C),
                                                          5790, 350, 220, 400),
                           sprites.VerticalMovingPlatform(images.get_platform(images.PIPE_Y, 90, 440, images.PIPE_Y_C),
                                                          5975, 300, 200, 390)]
        level_pipes = [sprites.Pipe(Level1_1(self.player, self), -350, 1776),
                       sprites.Pipe(None, 0, 2845, 0),
                       sprites.Pipe(Level1_2(self.player, self), 0, 5880, 339,
                                    images.get_platform(images.PIPE_B, 95, 215, images.PIPE_B_C))]
        level_blocks = [sprites.BreakableBlock(710, 135), sprites.BreakableBlock(802, 135),
                        sprites.BreakableBlock(1877, 48), sprites.Block(None, 2846, 396),
                        sprites.Block(None, 2892, 396), sprites.QBlock(756, 135, sprites.Reward(None)),
                        sprites.QBlock(1923, 48, sprites.Coin(1923, 48)), sprites.BreakableBlock(6313, 170),
                        sprites.QBlock(6267, 170, sprites.Reward(None))]
        level_enemies = [sprites.Goomba(831, 270), sprites.Koopa(3002, 358), sprites.Koopa(3400, 358)]

        star0 = sprites.StarCoin(1615, 418, 0)
        star2 = sprites.StarCoin(5220, 0, 2)
        self.star_coins.add(star0)
        self.star_coins.add(star2)
        level_coins = [sprites.Coin(720, 42), sprites.Coin(759, 3), sprites.Coin(796, 42), sprites.Coin(1070, 205),
                       sprites.Coin(1210, 160), sprites.Coin(1412, 205), sprites.Coin(1950, 455),
                       sprites.Coin(1997, 455), sprites.Coin(2042, 455), sprites.Coin(2090, 455),
                       sprites.Coin(3104, 270), sprites.Coin(3146, 225), sprites.Coin(3200, 225),
                       sprites.Coin(3240, 270), sprites.Coin(3545, 268), sprites.Coin(4210, 0, True, 0),
                       sprites.Coin(4255, 0, True, 0), sprites.Coin(4300, 0, True, 0), star0, star2]

        # Go through the arrays above and add platforms
        utils.add_all(level_platforms, self.platform_list, None, self.player)
        utils.add_all(level_pipes, self.platform_list, self, self.player)
        utils.add_all(level_enemies, self.enemy_list, None, self.player)
        utils.add_all(level_coins, self.reward_list)
        for aBlock in level_blocks:
            self.block_list.add(aBlock)
            if isinstance(aBlock, sprites.BreakableBlock):
                aBlock.level = self

    def load_sound(self):
        utils.change_sound(constants.PATH + 'level1_sound.mp3')


class Level1_1(level.SubLevel):
    def __init__(self, player, over_level):
        super().__init__(player, over_level)
        self.background = pygame.image.load(constants.PATH + "background_l1-1.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 1
        self.number = 0

        platforms = sprites.Platform(pygame.image.load(constants.PATH + "level_1-1.png"), 0, 0)
        platforms.player = self.player
        self.platform_list.add(platforms)

        pipe = sprites.Pipe(over_level, 2445, 3774, 336,
                            images.get_platform(images.PIPE_G, images.PIPE_G.get_rect().width, 225, images.PIPE_G_C))
        pipe.level = self
        pipe.player = self.player
        self.platform_list.add(pipe)
        star1 = sprites.StarCoin(2265, 95, 1)
        over_level.star_coins.add(star1)

        level_blocks = [sprites.BreakableBlock(925, 297), sprites.QBlock(971, 297, sprites.Reward(None)),
                        sprites.BreakableBlock(1017, 297), sprites.BreakableBlock(3192, 201),
                        sprites.QBlock(3238, 201, sprites.Reward(None))]

        level_enemies = [sprites.Goomba(969, 439), sprites.Goomba(1078, 439), sprites.Spike(2159, 76),
                         sprites.Spike(2472, 77)]

        level_walls = [sprites.ClimbingWall(2121, 297, images.get_platform(images.WALL, 96, 220, images.WALL_C,
                                                                           images.WALL_B)),
                       sprites.ClimbingWall(2290, 330), sprites.ClimbingWall(2451, 297, images.get_platform(
                         images.WALL, 96, 220, images.WALL_C, images.WALL_B)), sprites.ClimbingWall(2617, 260),
                       sprites.ClimbingWall(3109, 323), sprites.ClimbingWall(3280, 323)]

        level_coins = [sprites.Coin(925, 148), sprites.Coin(950, 105), sprites.Coin(990, 105), sprites.Coin(1015, 148),
                       sprites.Coin(1707, 265), sprites.Coin(1830, 160), sprites.Coin(1975, 255),
                       sprites.Coin(2127, 310), sprites.Coin(2178, 358), sprites.Coin(2127, 400),
                       sprites.Coin(2178, 455), sprites.Coin(2510, 310), sprites.Coin(2458, 358),
                       sprites.Coin(2510, 400), sprites.Coin(2458, 455), sprites.Coin(3200, 270),
                       sprites.Coin(3245, 270), sprites.Coin(3200, 90), sprites.Coin(3245, 90), sprites.Coin(3782, 285),
                       sprites.Coin(3830, 285), star1]

        for aBlock in level_blocks:
            self.block_list.add(aBlock)
            if isinstance(aBlock, sprites.BreakableBlock):
                aBlock.level = self
        utils.add_all(level_enemies, self.enemy_list, None, self.player)
        utils.add_all(level_walls, self.wall_list)
        utils.add_all(level_coins, self.reward_list)


class Level1_2(level.SubLevel):
    def __init__(self, player, over_level):
        super().__init__(player, over_level)
        self.background = pygame.image.load(constants.PATH + "background_l1.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 0
        self.number = 0

        platforms = sprites.Platform(pygame.image.load(constants.PATH + "level_1-2.png"), 0, 0)
        platforms.player = self.player
        self.platform_list.add(platforms)

        level_enemies = [sprites.Koopa(612, 373),
                         sprites.Koopa(729, 303),
                         sprites.Koopa(852, 223)]

        utils.add_all(level_enemies, self.enemy_list, None, self.player)
        self.add_flag(25)

    def load_sound(self):
        utils.change_sound(constants.PATH + 'level1_sound.mp3')
