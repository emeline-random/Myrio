import pygame

import utils
from sprites import MovingSprite
import images
import constants
import sprites


class Player(MovingSprite):

    def __init__(self):
        super().__init__(images.MARIO_STOP_B)
        self.jump_number = 0
        self.in_pipe = False
        self.pipe = None
        self.size = 3
        self.lives = 5
        self.climbing = False
        self.swimming = False
        self.moving = True
        self.frame = 0
        self.current = 0
        self.images = images.MARIO_BIG_R
        self.mask = pygame.mask.from_surface(images.MARIO)

    def current_image(self, n, img):
        if n < 0:
            self.image = img
        else:
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
        if self.swimming:
            self.calc_gravity(constants.UNDERWATER_GRAVITY)
        elif not self.climbing:
            self.calc_gravity()

        if self.in_pipe:  # Si le joueur est dans un tuyau il ne peut en sortir par les côtés
            self.change_x = 0
            self.rect.x = self.pipe.rect.x + (self.pipe.rect.width - self.rect.width) // 2
            if self.rect.y + self.rect.height < self.pipe.rect.y:  # si le joueur est au dessus de tuyau il en sort
                self.in_pipe = False

        self.rect.x += self.change_x
        # See if we hit anything
        if not self.climbing:
            for platform in sprites.sprite_collide(self, constants.CURRENT_LEVEL.platform_list):
                platform.update_constants()
                self.x_change(platform)
            for block in sprites.sprite_collide(self, constants.CURRENT_LEVEL.block_list):
                block.update_constants()
                self.x_change(block)
        elif not pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.wall_list, False):
            self.climbing = False

        self.rect.y += self.change_y
        # See if we hit anything
        if not self.climbing:
            platform_hit_list = sprites.sprite_collide(self, constants.CURRENT_LEVEL.platform_list)
            block_hit_list = sprites.sprite_collide(self, constants.CURRENT_LEVEL.block_list)
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

        if self.rect.y > constants.HEIGHT:  # see if we're falling
            self.decrease_size()

        # Looking if we hit an enemy or a reward
        for enemy in sprites.sprite_collide(self, constants.CURRENT_LEVEL.enemy_list):
            enemy.update_constants()
        for reward in sprites.sprite_collide(self, constants.CURRENT_LEVEL.reward_list):
            reward.update_constants()

    def x_change(self, platform):
        if self.change_x > 0:
            while pygame.sprite.collide_mask(platform, self):
                self.rect.x -= 1
        elif self.change_x < 0:
            while pygame.sprite.collide_mask(platform, self):
                self.rect.x += 1

    def decrease_size(self):
        self.size -= 1
        if self.size == 1:
            self.change_rect(images.MARIO_LITTLE)
        elif self.size == 0:
            utils.play_effect(utils.MARIO_DIES)

    def increase_size(self):
        self.size += 1
        if self.size > 3:
            self.size = 3
        elif self.size == 2:
            self.change_rect(images.MARIO)

    def add_life(self):
        self.lives += 1

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.lives = 5

    def change_rect(self, image):
        self.mask = pygame.mask.from_surface(image)
        y = self.rect.bottom
        x = self.rect.x
        self.rect = image.get_rect()
        self.rect.y = y - self.rect.height - 10
        self.rect.x = x

    def jump(self):
        # move down a bit and see if there is a platform below us.
        if not self.swimming:
            self.climbing = False
            self.rect.y += 2
            platform_hit_list = sprites.sprite_collide(self, constants.CURRENT_LEVEL.platform_list)
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
        else:
            self.go_up()

    def go_left(self):
        self.change_x = -constants.PLAYER_SPEED

    def go_right(self):
        self.change_x = constants.PLAYER_SPEED

    def go_down(self):
        self.change_y = constants.PLAYER_SPEED * 1.5

    def go_up(self):
        if pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.wall_list, False):
            self.climbing = True
            self.jump_number = 0
            self.change_y = -constants.PLAYER_SPEED
        elif self.swimming:
            self.change_y = -constants.PLAYER_SPEED

    def stop(self, x=True, y=True):
        if x:
            self.change_x = 0
        if y:
            self.change_y = 0
        if self.change_x == 0 and self.change_y == 0:
            self.moving = False

    def set_swim(self, boolean):
        self.swimming = boolean
        if self.swimming:
            self.change_rect(images.MARIO_SWIM)
            constants.PLAYER_SPEED = constants.UNDERWATER_SPEED
        else:
            self.change_rect(images.MARIO)
            constants.PLAYER_SPEED = constants.NORMAL_SPEED
