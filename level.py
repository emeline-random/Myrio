import pygame
import constants
import sprites as blocks
from sprites import Flag
import images


class Level:

    def __init__(self, player):
        self.player = player
        self.background = None
        self.world_shift = 0
        self.background_shift = 0
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.reward_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.max_frames = None
        self.current_frame = 0
        self.number = -1

    def begin(self):
        pass

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.reward_list.update()
        self.block_list.update()
        self.wall_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """
        screen.fill(constants.WHITE)
        if 0 <= self.background_shift // 3 <= constants.WIDTH:
            screen.blit(self.background, (self.background_shift // 3, 0))
            screen.blit(self.background, (-constants.WIDTH + self.background_shift // 3, 0))
        else:
            if self.background_shift // 3 < - constants.WIDTH:
                self.background_shift = 0
                self.current_frame += 1
            elif self.world_shift // 3 > constants.WIDTH:
                self.background_shift = 0
                self.current_frame -= 1
            screen.blit(self.background, (self.background_shift // 3, 0))
            screen.blit(self.background, (constants.WIDTH + self.background_shift // 3, 0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.reward_list.draw(screen)
        self.block_list.draw(screen)
        self.wall_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """
        self.world_shift += shift_x
        self.background_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for reward in self.reward_list:
            reward.rect.x += shift_x

        for block in self.block_list:
            block.rect.x += shift_x

        for wall in self.wall_list:
            wall.rect.x += shift_x

    def add_flag(self, next_level):
        flag = Flag(next_level)
        flag.rect.x = constants.WIDTH * (1 + self.max_frames * 3)
        flag.rect.y = constants.HEIGHT - flag.rect.height
        self.platform_list.add(flag)


class Level02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """
        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("data/background2.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.max_frames = 1
        self.number = 1

        # Array with type of platform, and x, y location of the platform.
        level = [[images.PLATFORM, 500, 500],
                 [images.PLATFORM, 533, 500],
                 [images.PLATFORM, 566, 500],
                 [images.PLATFORM, 800, 400],
                 [images.PLATFORM, 833, 400],
                 [images.PLATFORM, 866, 400],
                 [images.PLATFORM, 1000, 500],
                 [images.PLATFORM, 1033, 500],
                 [images.PLATFORM, 1066, 500],
                 [images.PLATFORM, 1120, 280],
                 [images.PLATFORM, 1153, 280],
                 [images.PLATFORM, 1186, 280]]

        # Go through the array above and add platforms
        for platform in level:
            block = blocks.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = blocks.HorizontalMovingPlatform(images.PLATFORM)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
