import pygame
import constants


class ImagesSheet:

    def __init__(self, file_name):
        self.sheet = pygame.image.load(file_name)

    def getimage(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.WHITE)
        return image

    def get_images(self, number, height, width, y):
        images = []
        for i in range(number):
            images.append(self.getimage(i * width, y, width, height))
        return images


def get_platform(image, width, height=None, center_image=None, bottom_image=None):
    if not height:
        surface = pygame.Surface((width, image.get_rect().height), pygame.SRCALPHA)
        i = 0
        while i < width:
            surface.blit(image, (i, 0))
            i += image.get_rect().width
    else:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        i = 0
        while i < width:
            surface.blit(image, (i, 0))
            i += image.get_rect().width
        j = image.get_rect().height
        while j < height:
            i = 0
            while i < width:
                surface.blit(center_image, (i, j))
                i += center_image.get_rect().width
            j += center_image.get_rect().height
        i = 0
        if bottom_image:
            while i < width:
                surface.blit(bottom_image, (i, surface.get_rect().height - bottom_image.get_rect().height))
                i += image.get_rect().width

    return surface


def get_blocks(image, number):
    surface = pygame.Surface((image.get_rect().width * number, image.get_rect().height), pygame.SRCALPHA)
    for i in range(number):
        surface.blit(image, (i * image.get_rect().width, 0))
    return surface


def empiled_blocks(image, number):
    surface = pygame.Surface((image.get_rect().width, image.get_rect().height * number), pygame.SRCALPHA)
    for i in range(number):
        surface.blit(image, (0, image.get_rect().height * i))
    return surface


sheet = ImagesSheet("data/mario.png")
MARIO_RIGHT = sheet.get_images(25, 90, 68, 22)
MARIO_LEFT = sheet.get_images(25, 90, 68, 126)
MARIO_JUMP = sheet.getimage(1019, 3, 71, 89)
MARIO_CLIMB = sheet.get_images(14, 81, 48, 227)
SWIM_R = sheet.get_images(14, 73, 71, 691)
SWIM_L = sheet.get_images(14, 73, 71, 764)
MARIO_STOP = sheet.getimage(707, 220, 53, 90)
MARIO_STOP_L = sheet.getimage(926, 247, 38, 58)
MARIO_STOP_B = sheet.getimage(988, 215, 86, 90)
MARIO_LITTLE_R = sheet.get_images(14, 60, 50, 335)
MARIO_LITTLE_L = sheet.get_images(14, 60, 50, 400)
MARIO_BIG_R = sheet.get_images(14, 90, 68, 467)
MARIO_BIG_L = sheet.get_images(14, 90, 68, 570)
MARIO = sheet.getimage(778, 217, 70, 98)
MARIO_LITTLE = sheet.getimage(852, 244, 60, 73)
MARIO_SWIM = sheet.getimage(1097, 236, 87, 71)


def get_mario(player):
    if not player.moving:
        player.frame = 0
        if player.climbing:
            player.image = MARIO_CLIMB[0]
        elif player.swimming:
            player.image = SWIM_R[0]
        elif player.size == 2:
            player.image = MARIO_STOP
        elif player.size == 1:
            player.image = MARIO_STOP_L
        else:
            player.image = MARIO_STOP_B
        return
    elif player.climbing:
        player.current_image(0, MARIO_CLIMB)
    elif player.swimming:
        if constants.GO_RIGHT == constants.CURRENT_DIR:
            player.current_image(2.3, SWIM_R)
        elif constants.GO_LEFT == constants.CURRENT_DIR:
            player.current_image(3.3, SWIM_L)
        else:
            player.current_image(player.current, None)
    elif constants.GO_RIGHT == constants.CURRENT_DIR:  # choosing adapted image depending on the current direction
        if player.size == 2:
            player.current_image(2, MARIO_RIGHT)
        elif player.size == 1:
            player.current_image(2.1, MARIO_LITTLE_R)
        else:
            player.current_image(2.2, MARIO_BIG_R)
    elif constants.GO_LEFT == constants.CURRENT_DIR:
        if player.size == 2:
            player.current_image(3, MARIO_LEFT)
        elif player.size == 1:
            player.current_image(3.1, MARIO_LITTLE_L)
        else:
            player.current_image(3.2, MARIO_BIG_L)
    player.image = player.images[player.frame]


sheet = ImagesSheet("data/sprites_2.png")
LEVEL = sheet.getimage(638, 16, 82, 49)
FLAG_IMAGE = sheet.getimage(1341, 30, 156, 484)
KOOPA_LEFT = sheet.getimage(85, 1, 62, 79)
KOOPA_RIGHT = sheet.getimage(150, 1, 62, 79)
GOOMBA_LEFT = sheet.getimage(279, 5, 64, 44)
GOOMBA_RIGHT = sheet.getimage(242, 6, 36, 44)
CHEEP_LEFT = sheet.getimage(1038, 315, 47, 46)
CHEEP_RIGHT = sheet.getimage(1092, 315, 47, 46)
SPIKE = sheet.getimage(1195, 5, 84, 131)
SPIKE_BOMB = sheet.getimage(1201, 233, 84, 84)
HURCHIN = sheet.getimage(1178, 343, 115, 115)
BIG_HURCHIN = sheet.getimage(341, 580, 310, 287)
PYRANA_PLANT = sheet.getimage(665, 480, 52, 256)
PLATFORM = sheet.getimage(580, 179, 46, 24)
PLATFORM_Y = sheet.getimage(943, 231, 200, 45)
BLOCK = sheet.getimage(259, 179, 46, 47)
Q_BLOCK = sheet.getimage(214, 179, 46, 47)
BREAK_BLOCK = sheet.getimage(168, 179, 46, 47)
CHAMPI = sheet.getimage(355, 33, 55, 53)
PIPE_BLOCK = sheet.getimage(351, 455, 92, 90)
PIPE = sheet.getimage(160, 313, 91, 137)
PIPE_G = sheet.getimage(161, 314, 90, 57)
PIPE_G_C = sheet.getimage(161, 370, 90, 46)
PIPE_G_B = sheet.getimage(161, 416, 90, 35)
PIPE_R = sheet.getimage(626, 317, 90, 57)
PIPE_R_C = sheet.getimage(626, 374, 90, 46)
PIPE_R_B = sheet.getimage(626, 420, 90, 35)
PIPE_Y = sheet.getimage(59, 346, 90, 57)
PIPE_Y_C = sheet.getimage(59, 402, 90, 46)
PIPE_Y_B = sheet.getimage(59, 448, 90, 35)
PIPE_B = sheet.getimage(908, 317, 95, 55)
PIPE_B_C = sheet.getimage(908, 374, 95, 35)
PIECE = sheet.getimage(813, 89, 38, 45)
STAR_PIECE = sheet.getimage(762, 500, 129, 126)
STAR_PIECE_L = sheet.getimage(911, 505, 46, 45)
sheet = ImagesSheet("data/level_1.png")
GROUND = sheet.getimage(0, 0, 142, 70)
GROUND_C = sheet.getimage(0, 22, 142, 48)
FLOWERS = sheet.getimage(0, 78, 190, 119)
FLOWERS_C = sheet.getimage(0, 200, 190, 65)
FLOWERS_B = sheet.getimage(0, 270, 190, 30)
COLUMN = sheet.getimage(154, 1, 46, 47)
COLUMN_C = sheet.getimage(212, 0, 46, 72)
COLUMN_B = sheet.getimage(154, 49, 46, 25)
sheet = ImagesSheet("data/gake.png")
WALL = sheet.getimage(289, 72, 95, 25)
WALL_C = sheet.getimage(289, 97, 95, 46)
WALL_B = sheet.getimage(289, 146, 95, 16)
