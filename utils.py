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
