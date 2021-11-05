import pygame

SPEED = 3
IMG_SIZE = (60, 60)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        enemy_img = pygame.transform.scale(pygame.image.load('assets/enemy.png'), IMG_SIZE).convert_alpha()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, speed):
        self.rect.centerx -= int(speed)
