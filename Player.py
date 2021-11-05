import pygame

WHITE = (255, 255, 255)
GRAVITY = 0.1
JUMP_HEIGHT = 5.2
IMG_SIZE = (100, 80)
ANIMATION_SPEED = 0.03


class Player(pygame.sprite.Sprite):
    movement = GRAVITY

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [
            pygame.transform.scale(pygame.image.load('assets/player_frames/frame_0.gif'), IMG_SIZE).convert_alpha(),
            pygame.transform.scale(pygame.image.load('assets/player_frames/frame_1.gif'), IMG_SIZE).convert_alpha(),
            pygame.transform.scale(pygame.image.load('assets/player_frames/frame_2.gif'), IMG_SIZE).convert_alpha(),
            pygame.transform.scale(pygame.image.load('assets/player_frames/frame_3.gif'), IMG_SIZE).convert_alpha()
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += ANIMATION_SPEED
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.centery += self.movement  # update the position with the current movement
        self.movement += GRAVITY            # update the movement with gravity for the next draw

    def jump(self):
        self.movement = 0
        self.movement -= JUMP_HEIGHT
