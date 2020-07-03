import pygame

import constants
from sprites import MovingSprite
import sprites
import images


class Player(MovingSprite):

    def __init__(self):
        super().__init__(images.MARIO)
        self.change_x = 0
        self.change_y = 0
        self.jump_number = 0
        self.in_pipe = False
        self.pipe = None
        self.life = 3
        self.climbing = False
        self.frame = 0
        self.current = 0
        self.images = images.MARIO_RIGHT
        self.moving = True

    def current_image(self, n, img):
        if self.current == n:
            self.frame += 1
            if len(self.images) < self.frame + 1:
                self.frame = 0
        else:
            self.images = img
            self.frame = 0
            self.current = n

    def update(self):
        images.get_mario(self)
        if not self.climbing:
            self.calc_gravity()

        if self.in_pipe:  # Si le joueur est dans un tuyau il ne peut en sortir par les côtés
            self.change_x = 0
            self.rect.x = self.pipe.rect.x + (self.pipe.rect.width - self.rect.width) // 2
            if self.rect.y + self.rect.height < self.pipe.rect.y:  # si le joueur est au dessus de tuyau il en sort
                self.in_pipe = False

        self.rect.x += self.change_x
        # See if we hit anything
        if not self.climbing:
            for platform in sprites.spritecollide(self, constants.CURRENT_LEVEL.platform_list):
                platform.update_constants()
                self.x_change(platform)
            for block in sprites.spritecollide(self, constants.CURRENT_LEVEL.block_list):
                block.update_constants()
                self.x_change(block)
        elif not pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.wall_list, False):
            self.climbing = False

        self.rect.y += self.change_y
        # See if we hit anything
        if not self.climbing:
            platform_hit_list = sprites.spritecollide(self, constants.CURRENT_LEVEL.platform_list)
            block_hit_list = sprites.spritecollide(self, constants.CURRENT_LEVEL.block_list)
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
        elif not pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.wall_list, False):
            self.climbing = False

        # Looking if we hit an enemy or a reward
        for enemy in sprites.spritecollide(self, constants.CURRENT_LEVEL.enemy_list):
            enemy.update_constants()
        for reward in sprites.spritecollide(self, constants.CURRENT_LEVEL.reward_list):
            reward.update_constants()

    def x_change(self, platform):
        if self.change_x > 0:
            while pygame.sprite.collide_mask(platform, self):
                self.rect.x -= 1
        elif self.change_x < 0:
            while pygame.sprite.collide_mask(platform, self):
                self.rect.x += 1

    def kill(self):
        exit(0)

    def remove_life(self):
        if self.life == 0:
            self.kill()
        else:
            self.mask = pygame.mask.from_surface(images.MARIO_LITTLE)
            y = self.rect.y
            x = self.rect.x
            self.rect = images.MARIO_LITTLE.get_rect()
            self.rect.y = y
            self.rect.x = x
            self.life -= 1

    def add_life(self):
        self.life = 3
        self.mask = pygame.mask.from_surface(images.MARIO)
        y = self.rect.y
        x = self.rect.x
        self.rect = images.MARIO.get_rect()
        self.rect.y = y - 50
        self.rect.x = x

    def jump(self):
        # move down a bit and see if there is a platform below us.
        self.climbing = False
        self.rect.y += 2
        platform_hit_list = sprites.spritecollide(self, constants.CURRENT_LEVEL.platform_list)
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

    def go_up(self):
        if pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.wall_list, False):
            self.climbing = True
            self.change_y = -constants.PLAYER_SPEED

    def stop(self):
        self.change_x = 0
        self.change_y = 0
        self.moving = False
