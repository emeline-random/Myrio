import os

import pygame

import constants


def change_level(next_level):
    constants.CURRENT_LEVEL = next_level
    next_level.begin()


def add_all(sprites, sprites_list, level=None, player=None):
    if level is not None:
        for sprite in sprites:
            sprite.level = level
    if player is not None:
        for sprite in sprites:
            sprite.player = player
    for sprite in sprites:
        sprites_list.add(sprite)


sound_library = {}
MARIO_DIES = constants.PATH + 'mario_dies_2.wav'
PIPE = constants.PATH + 'pipe.wav'
KICK = constants.PATH + 'kick.wav'
POWER_UP = constants.PATH + 'powerup.wav'
STAGE_CLEAR = constants.PATH + 'stage_clear.wav'
COIN = constants.PATH + 'coin.wav'
BLOCK_BREAKS = constants.PATH + 'block_breaks.wav'


def play_effect(path):
    global sound_library
    sound = sound_library.get(path)
    if sound is None:
        canonicalize_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalize_path)
        sound_library[path] = sound
    sound.play()


def change_sound(sound_path):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)
