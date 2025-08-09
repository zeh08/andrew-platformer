import sys
import json
from pathlib import Path
import pygame
import numpy as np

from settings import WIDTH, HEIGHT, FPS
from level import Level

BASE_DIR = Path(__file__).resolve().parents[1]
LEVELS_DIR = BASE_DIR / 'levels'
SAVE_PATH = BASE_DIR / 'save.json'

LEVEL_FILES = [
    LEVELS_DIR / 'level1.txt',
    LEVELS_DIR / 'level2.txt',
]


def generate_tone(freq=440.0, duration=0.15, volume=0.4, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    audio = (wave * (2**15 - 1) * volume).astype(np.int16)
    stereo = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo)


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont('consolas', 48)
        self.font_small = pygame.font.SysFont('consolas', 24)

        self.current_level_index = 0
        self.level = None

        self.sfx = {
            'jump': generate_tone(700, 0.1, 0.3),
            'coin': generate_tone(1200, 0.1, 0.35),
            'dead': generate_tone(200, 0.25, 0.4),
            'complete': generate_tone(880, 0.2, 0.4),
            'click': generate_tone(500, 0.05, 0.3),
        }

        self.load_progress()
        self.load_level(self.current_level_index)

    def load_progress(self):
        if SAVE_PATH.exists():
            try:
                data = json.loads(SAVE_PATH.read_text(encoding='utf-8'))
                self.current_level_index = int(data.get('level', 0))
            except Exception:
                self.current_level_index = 0
        else:
            self.current_level_index = 0

    def save_progress(self):
        data = {'level': self.current_level_index}
        SAVE_PATH.write_text(json.dumps(data), encoding='utf-8')

    def load_level(self, idx: int):
        idx = max(0, min(idx, len(LEVEL_FILES) - 1))
        self.current_level_index = idx
        self.level = Level(LEVEL_FILES[idx])
        self.level.on_jump = lambda: self.sfx['jump'].play()

    def draw_centered_text(self, lines, y_start=HEIGHT // 2 - 60):
        for i, text in enumerate(lines):
            surf = self.font_large.render(text, True, (255, 255, 255))
            rect = surf.get_rect(center=(WIDTH // 2, y_start + i * 60))
            self.screen.blit(surf, rect)

        hint = self.font_small.render('按 Enter 开始 / Esc 退出', True, (230, 230, 230))
        rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.screen.blit(hint, rect)

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.sfx['click'].play()
                        return 'start'
                    if event.key == pygame.K_ESCAPE:
                        return 'quit'

            self.screen.fill((30, 30, 40))
            self.draw_centered_text(['迷你平台游戏', f'继续第 {self.current_level_index + 1} 关'])
            pygame.display.flip()
            self.clock.tick(FPS)

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_progress()
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_progress()
                    return 'menu'

            keys = pygame.key.get_pressed()

            status = self.level.run(self.screen, keys)

            if status == 'complete':
                self.sfx['complete'].play()
                pygame.time.delay(300)
                if self.current_level_index < len(LEVEL_FILES) - 1:
                    self.current_level_index += 1
                    self.save_progress()
                    self.load_level(self.current_level_index)
                else:
                    return 'win'
            elif status == 'dead':
                self.sfx['dead'].play()
                pygame.time.delay(400)
                self.load_level(self.current_level_index)

            pygame.display.flip()
            self.clock.tick(FPS)
        return 'quit'

    def win_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.sfx['click'].play()
                        return 'menu'
                    if event.key == pygame.K_ESCAPE:
                        return 'quit'

            self.screen.fill((20, 90, 50))
            self.draw_centered_text(['恭喜通关！', '按 Enter 返回菜单'])
            pygame.display.flip()
            self.clock.tick(FPS)


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.display.set_caption('Mini Platformer')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game(screen)

    while True:
        action = game.main_menu()
        if action == 'quit':
            break
        if action == 'start':
            outcome = game.game_loop()
            if outcome == 'win':
                back = game.win_screen()
                if back == 'quit':
                    break
            elif outcome == 'menu':
                continue
            else:
                break

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
