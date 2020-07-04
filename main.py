import pygame

import constants
from level_1 import Level01

from player import Player


def main():
    """ Main Program """
    pygame.init()

    size = [constants.WIDTH, constants.HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dino game")
    player = Player()

    # Set the current level
    constants.CURRENT_LEVEL = Level01(player)
    constants.CURRENT_LEVEL.begin()

    active_sprite_list = pygame.sprite.Group()
    player.level = constants.CURRENT_LEVEL

    player.rect.x = 0
    player.rect.y = constants.HEIGHT - player.rect.height - 72
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                player.moving = True
                if event.key == pygame.K_LEFT:
                    player.go_left()
                    constants.CURRENT_DIR = constants.GO_LEFT
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                    constants.CURRENT_DIR = constants.GO_RIGHT
                if event.key == pygame.K_SPACE:
                    player.jump()
                    constants.CURRENT_DIR = constants.GO_UP
                if event.key == pygame.K_DOWN:
                    player.go_down()
                    constants.CURRENT_DIR = constants.GO_DOWN
                if event.key == pygame.K_UP:
                    player.go_up()
                    constants.CURRENT_DIR = constants.CLIMB

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop(True, False)
                elif event.key == pygame.K_UP and player.change_y < 0:
                    player.stop(False, True)
                elif event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop(False, True)
                elif event.key == pygame.K_SPACE and player.swimming:
                    player.stop(False, True)

        active_sprite_list.update()
        constants.CURRENT_LEVEL.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            constants.CURRENT_LEVEL.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            constants.CURRENT_LEVEL.shift_world(diff)

        constants.CURRENT_LEVEL.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
