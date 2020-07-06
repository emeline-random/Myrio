import pygame

import constants
from map import Map
from player import Player
import images


def change_level(level, player):
    constants.CURRENT_LEVEL = level
    constants.CURRENT_LEVEL.begin()
    player.rect.x = 50
    player.rect.y = constants.HEIGHT - player.rect.height - 200


def main():
    """ Main Program """
    pygame.init()

    size = [constants.WIDTH, constants.HEIGHT]
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font('data/font.ttf', 60)
    font_l = pygame.font.Font('data/font.ttf', 35)
    pygame.display.set_caption("Dino game")
    player = Player()
    constants.MAP = Map(player)

    # Set the current level
    constants.CURRENT_LEVEL = constants.MAP
    constants.CURRENT_LEVEL.begin()

    active_sprite_list = pygame.sprite.Group()
    player.level = constants.CURRENT_LEVEL

    player.rect.x = 50
    player.rect.y = constants.HEIGHT - player.rect.height - 200
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
        if player.rect.right >= 500 and constants.CURRENT_LEVEL != constants.MAP:
            diff = player.rect.right - 500
            player.rect.right = 500
            constants.CURRENT_LEVEL.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120 and constants.CURRENT_LEVEL != constants.MAP:
            diff = 120 - player.rect.left
            player.rect.left = 120
            constants.CURRENT_LEVEL.shift_world(diff)

        if player.size == 0:
            player.increase_size()
            constants.CURRENT_LEVEL.reset()
            change_level(constants.MAP, player)
            player.remove_life()

        constants.CURRENT_LEVEL.draw(screen)
        active_sprite_list.draw(screen)
        for star_coin in constants.CURRENT_LEVEL.star_coins:
            if star_coin.found:
                screen.blit(star_coin.image,
                            (star_coin.position * (images.STAR_PIECE_L.get_rect().width + 10) + 10, 10))
        coins = font.render(str(constants.COIN), True, (0, 0, 0))
        lives = font_l.render('x' + str(player.lives), True, (0, 0, 0))
        screen.blit(coins, (10, 150))
        screen.blit(lives, (10, 110))

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
