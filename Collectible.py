import pygame
import enum

IMG_SIZE = (80, 80)


class CollectibleTypes(enum.Enum):
    baguette = 'assets/collectibles/bag.png'
    apple = 'assets/collectibles/Apple.png'
    banana = 'assets/collectibles/Banana.png'
    peach = 'assets/collectibles/Peach.png'
    cherry = 'assets/collectibles/Cherry.png'
    watermelon = 'assets/collectibles/Watermelon.png'


class Collectible(pygame.sprite.Sprite):
    def __init__(self, collectible_type, pos_x, pos_y):
        super().__init__()
        collectible_image = pygame.transform.scale(pygame.image.load(collectible_type.value), IMG_SIZE).convert_alpha()
        self.image = collectible_image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, speed):
        self.rect.centerx -= int(speed)
