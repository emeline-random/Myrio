import pygame
import constants
import images
from sprites import Flag
from sprites import StarCoin


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
        self.star_coins = pygame.sprite.Group()
        self.lists = [self.platform_list, self.block_list, self.wall_list, self.enemy_list, self.reward_list]
        self.max_frames = None
        self.current_frame = 0
        self.number = -1

    def begin(self):
        self.player.climbing = False
        self.player.swimming = False
        self.player.jump_number = 0
        constants.PLAYER_SPEED = constants.NORMAL_SPEED
        if self.player.size > 1:
            self.player.change_rect(images.MARIO)
        else:
            self.player.change_rect(images.MARIO_LITTLE)

    def update(self):
        for aList in self.lists:
            aList.update()

    def draw(self, screen):
        """ Draw everything on this level. The background is drawn two times so that the entire screen is fill"""
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

        for aList in self.lists:
            aList.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """
        self.world_shift += shift_x
        self.background_shift += shift_x
        for aList in self.lists:
            for sprite in aList:
                sprite.rect.x += shift_x

    def add_flag(self, x):
        flag = Flag(x)
        flag.rect.x = constants.WIDTH * (self.max_frames * 3 + 0.75)
        flag.rect.y = constants.HEIGHT - flag.rect.height
        self.platform_list.add(flag)

    def reset(self):
        self.__init__(self.player)

    def end(self):
        coins = self.star_coins
        self.reset()
        for coin in coins:
            if coin.found:
                self.star_coins.add(coin)
                for c in self.reward_list:
                    if isinstance(c, StarCoin) and c.position == coin.position:
                        self.star_coins.remove(c)
                        self.reward_list.remove(c)
                        self.reward_list.add(coin)
                        break


class SubLevel(Level):
    def __init__(self, player, over_level):
        super().__init__(player)
        self.over_level = over_level
        self.star_coins = over_level.star_coins

    def reset(self):
        Level.reset(self.over_level)

    def end(self):
        Level.end(self.over_level)
