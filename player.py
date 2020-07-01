import pygame
import constants
from sprites import MovingSprite
import images


class Player(MovingSprite):

    def __init__(self):
        super().__init__(images.MARIO_RIGHT)
        self.change_x = 0
        self.change_y = 0
        self.jump_number = 0
        self.in_pipe = False
        self.pipe = None
        self.life = 3

    def update(self):
        self.calc_gravity()

        if self.in_pipe:  # Si le joueur est dans un tuyau il ne peut en sortir par les côtés
            self.change_x = 0
            self.rect.x = self.pipe.rect.x + (self.pipe.rect.width - self.rect.width) // 2
            if self.rect.y + self.rect.height < self.pipe.rect.y:  # si le joueur est au dessus de tuyau il en sort
                self.in_pipe = False

        if constants.GO_RIGHT == constants.CURRENT_DIR:  # choosing adapted image depending on the current direction
            self.image = images.MARIO_RIGHT
        elif constants.GO_LEFT == constants.CURRENT_DIR:
            self.image = images.MARIO_LEFT

        self.rect.x += self.change_x
        # See if we hit anything
        for platform in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.platform_list, False):
            platform.update_constants()
            self.x_change(platform)
        for block in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.block_list, False):
            block.update_constants()
            self.x_change(block)

        self.rect.y += self.change_y
        # See if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.platform_list, False)
        block_hit_list = pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.block_list, False)
        if len(platform_hit_list) > 0 or len(block_hit_list) > 0:
            self.jump_number = 0
        for platform in platform_hit_list:
            platform.update_constants()
            if not self.in_pipe:  # no verification if we're in a pipe
                self.y_change(platform)
        for block in block_hit_list:
            block.update_constants()
            if not self.in_pipe:  # no verification if we're in a pipe
                self.y_change(block)

        # Looking if we hit an enemy or a reward
        for enemy in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.enemy_list, False):
            enemy.update_constants()
        for reward in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.reward_list, False):
            reward.update_constants()

    def x_change(self, platform):
        if self.change_x > 0:
            self.rect.right = platform.rect.left
        elif self.change_x < 0:
            self.rect.left = platform.rect.right

    def kill(self):
        exit(0)

    def remove_life(self):
        if self.life == 0:
            self.kill()
        else:
            self.life -= 1

    def add_life(self):
        self.life += 1

    def jump(self):
        # move down a bit and see if there is a platform below us.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.HEIGHT:
            self.change_y = -constants.PLAYER_JUMP
            self.jump_number = 1
        elif self.jump_number == 0:
            self.jump_number = 1
            self.change_y = -constants.PLAYER_JUMP
        elif self.jump_number == 1:
            self.change_y = -constants.PLAYER_JUMP * 1.5
            self.jump_number = 2

    def go_left(self):
        self.change_x = -constants.PLAYER_SPEED

    def go_right(self):
        self.change_x = constants.PLAYER_SPEED

    def go_down(self):
        self.change_y = constants.PLAYER_SPEED * 1.5

    def stop(self):
        self.change_x = 0
