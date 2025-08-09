import pygame
from settings import TILE_SIZE, GROUND, GOAL_COLOR

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GROUND)
        self.rect = self.image.get_rect(topleft=pos)

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
