import pygame
from settings import PLAYER_SPEED, GRAVITY, JUMP_SPEED, TILE_SIZE, PLAYER_COLOR

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE // 2, int(TILE_SIZE * 0.9)))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.did_jump = False
        # Jump quality-of-life
        self.prev_jump_pressed = False
        self.jump_buffer_frames = 6
        self.jump_buffer_counter = 0
        self.coyote_frames = 6
        self.coyote_counter = 0
        self.jump_held = False

    def handle_input(self, keys):
        # Horizontal movement
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        # Jump buffer (edge trigger) + held state
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        self.jump_held = jump_pressed
        if jump_pressed and not self.prev_jump_pressed:
            self.jump_buffer_counter = self.jump_buffer_frames
        self.prev_jump_pressed = jump_pressed

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE_SIZE:  # clamp fall speed
            self.vel.y = TILE_SIZE

    def move_and_collide(self, tiles):
        # Horizontal
        self.rect.x += int(self.vel.x)
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right

        # Vertical
        self.apply_gravity()
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0

    def update(self, keys, tiles):
        # frame start
        self.did_jump = False
        # Update timers
        if self.on_ground:
            self.coyote_counter = self.coyote_frames
        elif self.coyote_counter > 0:
            self.coyote_counter -= 1
        if self.jump_buffer_counter > 0:
            self.jump_buffer_counter -= 1

        # Input and horizontal
        self.handle_input(keys)

        # Allow jump if grounded/coyote and either buffered edge or currently held
        if (self.on_ground or self.coyote_counter > 0) and (self.jump_buffer_counter > 0 or self.jump_held):
            self.vel.y = JUMP_SPEED
            self.on_ground = False
            self.did_jump = True
            self.jump_buffer_counter = 0
            self.coyote_counter = 0

        # Physics and collisions
        self.move_and_collide(tiles)
