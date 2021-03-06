import pygame

import images
import constants
import utils


def sprite_collide(sprite, group):
    return [s for s in group if pygame.sprite.collide_mask(s, sprite)]


class SolidShape(pygame.sprite.Sprite):

    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update_constants(self):
        pass


class MovingSprite(SolidShape):

    def __init__(self, image, x=0, y=0):
        super().__init__(image, x, y)
        self.speed = constants.DEFAULT_SPEED
        self.change_y = 0
        self.change_x = 0

    def calc_gravity(self, gravity=constants.GRAVITY):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += gravity

    def update(self, *args):
        self.calc_gravity()
        self.rect.y += self.change_y
        platforms = constants.CURRENT_LEVEL.platform_list
        blocks = constants.CURRENT_LEVEL.block_list
        for platform in sprite_collide(self, platforms):
            self.y_change(platform)
        for block in sprite_collide(self, blocks):
            self.y_change(block)
        self.rect.x += self.change_x
        if sprite_collide(self, platforms) or sprite_collide(self, blocks):
            self.rect.x -= self.change_x
            self.change_x *= -1

    def y_change(self, platform):
        if self.change_y > 0:
            while pygame.sprite.collide_mask(self, platform):
                self.rect.y -= 1
        elif self.change_y < 0:
            while pygame.sprite.collide_mask(self, platform):
                self.rect.y += 1
        self.change_y = 0


class Flag(SolidShape):

    def __init__(self, shift):
        super().__init__(images.FLAG_IMAGE)
        self.shift = shift
        self.reach = False

    def update_constants(self):
        self.reach = True
        utils.play_effect(utils.STAGE_CLEAR)
        if constants.CURRENT_LEVEL.player.rect.bottom < self.rect.y + 100:
            constants.CURRENT_LEVEL.player.add_life()
        constants.CURRENT_LEVEL.end()
        utils.change_level(constants.MAP)
        constants.CURRENT_LEVEL.shift_world = self.shift


class Platform(SolidShape):

    def __init__(self, image, x=0, y=0):
        super().__init__(image, x, y)
        self.boundary_left = 0
        self.boundary_right = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.level = None
        self.player = None


class HorizontalMovingPlatform(Platform, MovingSprite):

    def __init__(self, image, x=0, y=0, right=0, left=0):
        super().__init__(image, x, y)
        self.change_x = constants.BLOCK_SPEED
        self.boundary_right = right
        self.boundary_left = left

    def update(self):
        self.rect.x += self.change_x
        shift = constants.CURRENT_LEVEL.world_shift
        if self.rect.x <= self.boundary_left + shift or self.rect.right >= self.boundary_right + shift:
            self.change_x *= -1

    def update_constants(self):
        self.player.rect.x += self.change_x


class VerticalMovingPlatform(Platform):

    def __init__(self, image, x=0, y=0, top=0, bottom=0):
        super().__init__(image, x, y)
        self.change_y = constants.BLOCK_SPEED
        self.boundary_top = top
        self.boundary_bottom = bottom

    def update(self):
        self.rect.y += self.change_y
        if self.rect.top <= self.boundary_top or self.rect.top >= self.boundary_bottom:
            self.change_y *= -1

    def update_constants(self):
        self.player.rect.y += self.change_y


class Block(SolidShape):

    def __init__(self, image, x=0, y=0):
        if image is None:
            super().__init__(images.BLOCK, x, y)
        else:
            super().__init__(image, x, y)


class BreakableBlock(Block):

    def __init__(self, x=0, y=0, image=None):
        if image:
            super().__init__(image, x, y)
        else:
            super().__init__(images.BREAK_BLOCK, x, y)
        self.level = None

    def update_constants(self):
        pl_rect = constants.CURRENT_LEVEL.player.rect
        if pl_rect.y <= self.rect.bottom < pl_rect.bottom or constants.GO_DOWN == constants.CURRENT_DIR:
            utils.play_effect(utils.BLOCK_BREAKS)
            self.kill()


class QBlock(Block):

    def __init__(self, x=0, y=0, reward=None, down=False):
        super().__init__(images.Q_BLOCK, x, y)
        self.reward = reward
        self.down = down

    def update_constants(self):
        if self.reward is not None:
            if not self.down:
                pl_rect = constants.CURRENT_LEVEL.player.rect
                if constants.GO_DOWN == constants.CURRENT_DIR:
                    self.reward_out(self.rect.bottom + 1)
                elif pl_rect.y <= self.rect.bottom < pl_rect.bottom:
                    self.reward_out(self.rect.y - self.reward.rect.height - 1)
            else:
                self.reward_out(self.rect.bottom + 1)

    def reward_out(self, y):
        self.reward.player = constants.CURRENT_LEVEL.player
        self.reward.rect.y = y
        self.reward.rect.x = self.rect.x
        constants.CURRENT_LEVEL.reward_list.add(self.reward)
        self.reward.out = True
        self.image = images.BLOCK
        if isinstance(self.reward, Coin):
            self.reward.add_coin()
        self.reward = None


class Pipe(SolidShape):

    def __init__(self, relative_level, level_shift, x=0, y=constants.HEIGHT - images.PIPE.get_rect().height,
                 image=images.PIPE, y_in=None, top_pipe=False):
        super().__init__(image, x, y)
        self.relative_level = relative_level
        self.level_shift = level_shift
        self.on_left = False
        self.on_right = False
        self.player = None
        self.level = None
        self.top = top_pipe
        if not y_in:
            y_in = self.rect.bottom - 5
        self.y_in = y_in

    def update_constants(self):
        if self.top and constants.GO_UP == constants.CURRENT_DIR:
            self.go_in(self.player.rect.top <= self.y_in)
        elif constants.GO_DOWN == constants.CURRENT_DIR:
            self.go_in(self.player.rect.bottom >= self.y_in)

    def go_in(self, in_pipe):
        self.player.in_pipe = True
        self.player.pipe = self
        if in_pipe:
            utils.play_effect(utils.PIPE)
            utils.change_level(self.relative_level)
            self.player.pipe = None
            self.player.in_pipe = False
            constants.CURRENT_LEVEL.shift_world(-self.level_shift - constants.CURRENT_LEVEL.world_shift)


class ClimbingWall(SolidShape):
    def __init__(self, x, y, image=images.get_platform(images.WALL, 94, 89, images.WALL_C, images.WALL_B)):
        super(ClimbingWall, self).__init__(image, x, y)
        self.climbing = False


class Enemy(MovingSprite):

    def __init__(self, image_l, image_r, x=0, y=0, killable=True):
        self.killable = killable
        if image_l is not None:
            super().__init__(image_l, x, y)
        else:
            super().__init__(images.KOOPA_LEFT, x, y)
            image_l = images.GOOMBA_LEFT
            image_r = images.GOOMBA_RIGHT
        if not y:
            self.rect.y = constants.HEIGHT - self.rect.height
        self.change_x = -constants.ENEMY_SPEED
        self.player = None
        self.out = False
        self.image_l = image_l
        self.image_r = image_r
        self.eat = False

    def update(self):
        if (not self.out) and constants.CURRENT_LEVEL.world_shift <= constants.WIDTH - self.rect.x:
            self.out = True
        if self.out:
            if self.change_x > 0:
                self.image = self.image_r
            else:
                self.image = self.image_l
            super().update()
            constants.CURRENT_LEVEL.enemy_list.remove(self)
            if sprite_collide(self, constants.CURRENT_LEVEL.enemy_list):
                self.change_x *= -1
            constants.CURRENT_LEVEL.enemy_list.add(self)
            if not pygame.sprite.collide_mask(self, self.player):
                self.eat = False

    def update_constants(self):
        if self.player.rect.bottom - self.player.change_y <= self.rect.top + 20 and self.killable:
            utils.play_effect(utils.KICK)
            self.kill()
        elif not self.eat:
            self.eat = True
            self.player.decrease_size()


class Koopa(Enemy):
    def __init__(self, x, y=0):
        super().__init__(images.KOOPA_LEFT, images.KOOPA_RIGHT, x, y)


class Goomba(Enemy):
    def __init__(self, x, y=0):
        super().__init__(images.GOOMBA_LEFT, images.GOOMBA_RIGHT, x, y)


class Spike(Enemy):

    def __init__(self, x, y=0):
        super().__init__(images.SPIKE, None, x, y)
        self.change_x = 0
        self.thrown = False

    def update(self):
        if (not self.out) and constants.CURRENT_LEVEL.world_shift <= constants.WIDTH - self.rect.x:
            self.out = True
        if self.out:
            if self.change_x > 0:
                self.image = self.image_r
            else:
                self.image = self.image_l
            if not pygame.sprite.collide_mask(self, self.player):
                self.eat = False
            right = self.rect.right
            pl_rect = self.player.rect
            if (not self.thrown) and (self.rect.x < pl_rect.x < right or self.rect.x < pl_rect.right < right):
                self.thrown = True
                constants.CURRENT_LEVEL.enemy_list.add(SpikeBomb(self.player, self.rect.x, self.rect.y))
            elif not (self.rect.x < pl_rect.x < right or self.rect.x < pl_rect.right < right):
                self.thrown = False


class SpikeBomb(Enemy):

    def __init__(self, player, x, y=0):
        super().__init__(images.SPIKE_BOMB, None, x, y, False)
        self.change_x = 0
        self.change_y = constants.ENEMY_SPEED
        self.player = player

    def update(self):
        self.rect.y += self.change_y
        if self.rect.y > constants.HEIGHT:
            self.kill()


class Cheep(Enemy, HorizontalMovingPlatform):

    def __init__(self, x, y, right, left):
        Enemy.__init__(self, images.CHEEP_LEFT, images.CHEEP_RIGHT, x, y, False)
        HorizontalMovingPlatform.__init__(self, images.CHEEP_RIGHT, x, y, right, left)
        self.change_x = constants.ENEMY_SPEED


class Hurchin(Enemy, VerticalMovingPlatform):

    def __init__(self, x, y, top, bottom, big=False):
        if big:
            self.image_l = images.BIG_HURCHIN
        else:
            self.image_l = images.HURCHIN
        Enemy.__init__(self, self.image_l, None, x, y, False)
        self.change_x = 0
        VerticalMovingPlatform.__init__(self, self.image_l, x, y, top, bottom)
        self.change_y = constants.ENEMY_SPEED

    def update(self):
        VerticalMovingPlatform.update(self)


class Reward(MovingSprite):

    def __init__(self, image, x=0, y=0):
        if image is None:
            super().__init__(images.CHAMPI, x, y)
        else:
            super().__init__(image, x, y)
        self.change_x = -constants.REWARD_SPEED
        self.player = None
        self.out = False

    def update_constants(self):
        self.kill()
        self.player.increase_size()
        utils.play_effect(utils.POWER_UP)


class Coin(Reward):

    def __init__(self, x=0, y=0, moving=False, speed=-constants.REWARD_SPEED * 0.0001, image=images.PIECE):
        super().__init__(image, x, y)
        if not moving:
            self.change_x = 0
            self.change_y = 0
        else:
            self.change_x = speed
        self._moving = moving

    def update_constants(self):
        self.add_coin()

    def update(self):
        if self._moving:
            Reward.update(self)

    def add_coin(self):
        utils.play_effect(utils.COIN)
        self.kill()
        constants.COIN += 1
        if constants.COIN == 100:
            constants.CURRENT_LEVEL.player.add_life()
            constants.COIN = 0


class StarCoin(Coin):

    def __init__(self, x=0, y=0, position=0):
        super().__init__(x, y, False, None, images.STAR_PIECE)
        self.change_x = 0
        self.position = position
        self.found = False

    def update_constants(self):
        if not self.found:
            utils.play_effect(utils.COIN)
            self.rect.x = -100
            self.rect.y = -100
            self.image = images.STAR_PIECE_L
            self.found = True
        constants.CURRENT_LEVEL.reward_list.remove(self)

    def update(self):
        pass


class LevelRound(SolidShape):

    def __init__(self, x, y, level, shift=0):
        super().__init__(images.LEVEL, x, y)
        self.level = level
        self.shift = shift

    def update_constants(self):
        if constants.CURRENT_DIR == constants.GO_DOWN:
            self.level.shift_world(self.shift)
            self.level.begin()
            constants.CURRENT_LEVEL = self.level
