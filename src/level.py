from pathlib import Path
import pygame
from settings import TILE_SIZE, WIDTH, HEIGHT, SKY, TEXT_COLOR, UI_BG, UI_BG_ALPHA
from tiles import Tile, Goal
from player import Player

class Level:
    def __init__(self, level_path: Path):
        self.level_path = level_path
        self.level_map = self._load_map(level_path)
        self.cols = max(len(row) for row in self.level_map)
        self.rows = len(self.level_map)
        self.pixel_width = self.cols * TILE_SIZE
        self.pixel_height = self.rows * TILE_SIZE

        self.tiles = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.player = None

        self._build()

        self.offset = pygame.math.Vector2(0, 0)
        self.font = pygame.font.SysFont('consolas', 24)
        self.on_jump = None  # callback for jump sfx

    def _load_map(self, path: Path):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
        else:
            lines = [
                '--------------------------------',
                '--------------------------------',
                '---------------------XXXX-------',
                '-------------XXX----------------',
                '----------------------XX--------',
                '------XX------------------------',
                '---------------------------X----',
                '----------XX--------------------',
                '----------------------XXXX------',
                '----P-------------------------G-',
                '--------------------------------',
                'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            ]
        return lines

    def _build(self):
        for y, row in enumerate(self.level_map):
            for x, ch in enumerate(row):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                if ch == 'X':
                    self.tiles.add(Tile((world_x, world_y)))
                elif ch == 'P':
                    self.player = Player((world_x, world_y - TILE_SIZE))
                elif ch == 'G':
                    self.goals.add(Goal((world_x, world_y)))
        if self.player is None:
            # Fallback spawn at top-left if no 'P' found
            self.player = Player((TILE_SIZE, TILE_SIZE))

    def _compute_camera(self):
        # Center camera on player, clamp to level bounds
        px, py = self.player.rect.center
        ox = px - WIDTH // 2
        oy = py - HEIGHT // 2
        ox = max(0, min(ox, self.pixel_width - WIDTH))
        oy = max(0, min(oy, self.pixel_height - HEIGHT))
        self.offset.update(ox, oy)

    def _draw_hud(self, surface: pygame.Surface):
        # translucent bg bar
        hud_height = 36
        hud_surface = pygame.Surface((WIDTH, hud_height), pygame.SRCALPHA)
        hud_surface.fill((*UI_BG, UI_BG_ALPHA))
        text = f'Level: {self.level_path.stem}  Pos: {self.player.rect.x},{self.player.rect.y}'
        label = self.font.render(text, True, TEXT_COLOR)
        hud_surface.blit(label, (10, 6))
        surface.blit(hud_surface, (0, 0))

    def run(self, surface: pygame.Surface, keys):
        # Detect jump before update
        was_on_ground = self.player.on_ground

        # Update
        self.player.update(keys, self.tiles)
        if not was_on_ground and self.player.did_jump and self.on_jump:
            self.on_jump()
        elif was_on_ground and self.player.did_jump and self.on_jump:
            self.on_jump()
        self._compute_camera()

        # Check goal
        for goal in self.goals:
            if self.player.rect.colliderect(goal.rect):
                return 'complete'

        # Death if falling out of the world
        if self.player.rect.top > self.pixel_height + TILE_SIZE * 2:
            return 'dead'

        # Draw
        surface.fill(SKY)
        for tile in self.tiles:
            surface.blit(tile.image, tile.rect.topleft - self.offset)
        for goal in self.goals:
            surface.blit(goal.image, goal.rect.topleft - self.offset)
        surface.blit(self.player.image, self.player.rect.topleft - self.offset)
        self._draw_hud(surface)
        return 'running'
