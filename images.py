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


sheet = ImagesSheet("data/sprites.png")
FLAG_IMAGE = sheet.getimage(1341, 30, 156, 484)
KOOPA_LEFT = sheet.getimage(85, 1, 62, 81)
KOOPA_RIGHT = sheet.getimage(150, 2, 62, 81)
GOOMBA_LEFT = sheet.getimage(279, 5, 64, 44)
GOOMBA_RIGHT = sheet.getimage(242, 6, 36, 44)
PLATFORM = sheet.getimage(580, 179, 46, 24)
MARIO_RIGHT = sheet.getimage(418, 2, 71, 91)
MARIO_LEFT = sheet.getimage(918, 1, 71, 91)
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
PIPE_B = sheet.getimage(908, 317, 95, 57)
PIPE_B_C = sheet.getimage(908, 374, 95, 39)
PIECE = sheet.getimage(813, 89, 38, 45)
sheet = ImagesSheet("data/level_1.png")
GROUND = sheet.getimage(0, 0, 142, 70)
GROUND_C = sheet.getimage(0, 22, 142, 48)
FLOWERS = sheet.getimage(0, 78, 190, 119)
FLOWERS_C = sheet.getimage(0, 200, 190, 65)
FLOWERS_B = sheet.getimage(0, 270, 190, 30)
COLUMN = sheet.getimage(154, 1, 46, 47)
COLUMN_C = sheet.getimage(212, 0, 46, 72)
COLUMN_B = sheet.getimage(154, 49, 46, 25)
