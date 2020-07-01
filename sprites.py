import pygame

import constants
import images


class SolidShape(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_constants(self):
        pass


class MovingSprite(SolidShape):
    def __init__(self, image, x=0, y=0):
        super().__init__(image, x, y)
        self.speed = constants.DEFAULT_SPEED
        self.change_y = 0
        self.change_x = 0

    def calc_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += constants.GRAVITY

        # See if we are on the ground.
        if self.rect.y >= constants.HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.HEIGHT - self.rect.height

    def update(self, *args):
        self.calc_gravity()
        self.rect.x += self.change_x
        if pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.platform_list, False):
            self.change_x *= -1
        elif pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.block_list, False):
            self.change_x *= -1
        self.rect.y += self.change_y
        for platform in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.platform_list, False):
            self.y_change(platform)
        for block in pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.block_list, False):
            self.y_change(block)

    def y_change(self, platform):
        if self.change_y > 0:
            self.rect.bottom = platform.rect.top
        elif self.change_y < 0:
            self.rect.top = platform.rect.bottom
        self.change_y = 0


class Flag(SolidShape):
    def __init__(self, next_level):
        super().__init__(images.FLAG_IMAGE)
        self.next_level = next_level

    def update_constants(self):
        constants.CURRENT_LEVEL = self.next_level


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
        hit = pygame.sprite.collide_rect(self.player, self)
        if hit:
            if self.change_x > 0:  # moving right
                self.player.rect.left = self.rect.right
            else:  # moving left
                self.player.rect.right = self.rect.left
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
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:  # moving up
                self.player.rect.bottom = self.rect.top
        if self.rect.top <= self.boundary_top or self.rect.top >= self.boundary_bottom:
            self.change_y *= -1

    def update_constants(self):
        self.player.rect.y += self.change_y


class Pipe(SolidShape):

    def __init__(self, relative_level, level_shift, x=0, y=constants.HEIGHT - images.PIPE.get_rect().height,
                 image=images.PIPE):
        super().__init__(image, x, y)
        self.relative_level = relative_level
        self.level_shift = level_shift
        self.on_left = False
        self.on_right = False
        self.player = None
        self.level = None

    def update_constants(self):
        if constants.GO_DOWN == constants.CURRENT_DIR:
            self.player.in_pipe = True
            self.player.pipe = self
            if self.player.rect.y + self.player.rect.height >= self.rect.bottom - 5:
                constants.CURRENT_LEVEL = self.relative_level
                self.player.pipe = None
                self.player.in_pipe = False
                constants.CURRENT_LEVEL.shift_world(-self.level_shift - constants.CURRENT_LEVEL.world_shift)


class Enemy(MovingSprite):
    def __init__(self, image_l, image_r, x=0, y=0):
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
            if pygame.sprite.spritecollide(self, constants.CURRENT_LEVEL.enemy_list, False):
                self.change_x *= -1
            constants.CURRENT_LEVEL.enemy_list.add(self)
            if not pygame.sprite.collide_rect(self, self.player):
                self.eat = False

    def update_constants(self):
        if self.player.rect.bottom <= self.rect.top + 5:
            self.kill()
        elif not self.eat:
            self.eat = True
            self.player.remove_life()


class KoopaEnemy(Enemy):
    def __init__(self, x, y=0):
        super().__init__(images.KOOPA_LEFT, images.KOOPA_RIGHT, x, y)


class GoombaEnemy(Enemy):
    def __init__(self, x, y=0):
        super().__init__(images.GOOMBA_LEFT, images.GOOMBA_RIGHT, x, y)


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
        self.player.add_life()


class Piece(Reward):
    def __init__(self, x=0, y=0, image=images.PIECE):
        super().__init__(image, x, y)
        self.rect.y -= 10
        self.change_x = -constants.REWARD_SPEED * 0.0001

    def update_constants(self):
        self.add_piece()

    def add_piece(self):
        self.kill()
        constants.PIECES += 1


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
        if constants.GO_DOWN == constants.CURRENT_DIR and self.level.player.rect.bottom <= self.rect.y + 10:
            self.kill()
        elif constants.GO_UP == constants.CURRENT_DIR and self.level.player.rect.top >= self.rect.bottom - 10:
            self.kill()


class QBlock(Block):
    def __init__(self, x=0, y=0, reward=None):
        super().__init__(images.Q_BLOCK, x, y)
        self.reward = reward

    def update_constants(self):
        if self.reward is not None:
            if constants.GO_UP == constants.CURRENT_DIR and constants.CURRENT_LEVEL.player.rect.top >= self.rect.bottom - 10:
                self.reward_out(self.rect.y - self.reward.rect.height - 1)
            elif constants.GO_DOWN == constants.CURRENT_DIR and constants.CURRENT_LEVEL.player.rect.bottom <= self.rect.y + 10:
                self.reward_out(self.rect.bottom + 1)

    def reward_out(self, y):
        self.reward.player = constants.CURRENT_LEVEL.player
        self.reward.rect.y = y
        self.reward.rect.x = self.rect.x
        constants.CURRENT_LEVEL.reward_list.add(self.reward)
        self.reward.out = True
        self.image = images.BLOCK
        if isinstance(self.reward, Piece):
            self.reward.add_piece()
        self.reward = None
