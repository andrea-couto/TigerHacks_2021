# TigerHacks 2021 - SPACE!
# Copyright © 2021 Andy Couto

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# used Simple Space Effect by Silveira Neto for background with small changes found here:
# https://silveiraneto.net/2009/08/12/pygame-simple-space-effect/

import random
import pygame
import Player
import Collectible
import Enemy

NUMBER_OF_STARS = 200
NUMBER_OF_COLLECTIBLES = 30
SCREEN_W, SCREEN_H = (800, 800)
CENTER_W, CENTER_H = SCREEN_W / 2, SCREEN_H / 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCORE_PLACEMENT = (10, 10)
SUBTITLE_FONT_SIZE = 32
TITLE_FONT_SIZE = 48

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
background = pygame.Surface(screen.get_size())
star_values = [
    [random.uniform(0, SCREEN_W), random.uniform(0, SCREEN_H)]
    for _ in range(NUMBER_OF_STARS)
]


def game_over():
    game_over_font = pygame.font.Font('fonts/ZenKurenaido-Regular.ttf', TITLE_FONT_SIZE)
    restart_font = pygame.font.Font('fonts/ZenKurenaido-Regular.ttf', SUBTITLE_FONT_SIZE)

    game_over_text = game_over_font.render("GAME OVER", True, WHITE)
    restart_text = restart_font.render("tap `R` to restart", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(CENTER_W, CENTER_H - 60))
    restart_rect = restart_text.get_rect(center=(CENTER_W, CENTER_H))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)


def update_score(score_value):
    font = pygame.font.Font('fonts/ZenKurenaido-Regular.ttf', SUBTITLE_FONT_SIZE)
    score_text = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score_text, SCORE_PLACEMENT)


def draw_and_update_stars():
    for star in star_values:
        star_coordinate = (star[0], star[1])

        # draw the star with the current coordinates
        pygame.draw.line(background, WHITE, star_coordinate, star_coordinate)

        # update the coordinates for the next draw cycle
        star[0] = star[0] - 0.3  # move the star to the left
        if star[0] < 0:
            star[0] = SCREEN_W   # if the star will be off the screen, start it again all the way to the right
            star[1] = random.randint(0, SCREEN_H)  # and make it show up at a random y position


def create_collectibles(collectible_type):
    collectible_values = [
        (random.uniform(CENTER_W, SCREEN_W * 2), random.uniform(0, SCREEN_H))
        for _ in range(NUMBER_OF_COLLECTIBLES)
    ]
    collectibles = pygame.sprite.Group()

    for collectible_value in collectible_values:
        collectible = Collectible.Collectible(collectible_type, collectible_value[0], collectible_value[1])
        collectibles.add(collectible)
    return collectibles


def create_enemies(number_of_enemies):
    enemy_values = [
        (random.uniform(SCREEN_W, SCREEN_W * 20), random.uniform(0, SCREEN_H))
        for _ in range(number_of_enemies)
    ]
    enemies = pygame.sprite.Group()

    for enemy_value in enemy_values:
        enemy = Enemy.Enemy(enemy_value[0], enemy_value[1])
        enemies.add(enemy)
    return enemies


def main():
    number_of_enemies = 50
    speed = 3
    collectible_types = [c for c in Collectible.CollectibleTypes]
    is_game_over = False

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('TigerHacks 2021 - SPACE!')

    collectibles = create_collectibles(collectible_types[0])
    enemies = create_enemies(number_of_enemies)

    moving_sprites = pygame.sprite.Group()
    player = Player.Player(100, CENTER_H)
    moving_sprites.add(collectibles)
    moving_sprites.add(enemies)
    moving_sprites.add(player)

    score_value = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_r and is_game_over:
                    main()

        if player.rect.top > SCREEN_H or player.rect.bottom < 0:
            is_game_over = True
            game_over()
        if not is_game_over:
            # clear the background of what we did last draw cycle
            background.fill(BLACK)

            draw_and_update_stars()
            player.update()
            collectibles.update(speed)
            enemies.update(speed)

            screen.blit(background, (0, 0))
            moving_sprites.draw(screen)

            for collectible in collectibles:
                if player.rect.colliderect(collectible):
                    score_value += 1
                    collectible.kill()
                if collectible.rect.centerx < 0:
                    collectible.kill()

            for enemy in enemies:
                if player.rect.colliderect(enemy):
                    score_value -= 10
                    enemy.kill()
                if enemy.rect.centerx < 0:
                    enemy.kill()

            if len(collectibles) == 0:
                collectibles = create_collectibles(random.choice(collectible_types))
                moving_sprites.add(collectibles)
            if len(enemies) == 0:
                number_of_enemies += 5
                enemies = create_enemies(number_of_enemies)
                moving_sprites.add(enemies)

            update_score(score_value)
        speed += 0.003
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
