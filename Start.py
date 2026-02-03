import pygame
import sys
from settings import *


BG_GREEN = (86, 133, 97)      # The green background
WOOD_LIGHT = (244, 186, 96)   # Light wood color
WOOD_DARK = (194, 130, 51)    # D   
PAPER_COLOR = (242, 230, 194) # The paper inside the board
TEXT_COLOR = (255, 239, 213)  # Text color (light beige)
ICON_RED = (200, 50, 50)      # For the close button

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wooden Game Menu")

class MakeButton:
    def __init__(self, surface):
        self.surface = surface

    def on_init(self):
        pygame.init(SIZE)
        self._display_surface = pygame.display.set_mode()
    
        self._background_surface = pygame.Surface(SIZE)
        self._background_surface.fill((BG_GREEN))

    def draw(self):
        # rect button
        for y in range(100, 301, 100):
            pygame.draw.rect(self.surface, WOOD_LIGHT, (50, y, 220, 80), width = 3, border_radius = 5)

        # circle button
        radius = 3
        for x in range(150, WIDTH - 150 + 1, 50):
            rect = pygame.Rect(x, 500, 60, 60)
            center_rect = rect.center()
            radius = 60 // 2
            pygame.draw.circle(self.surface, WOOD_LIGHT, radius)

        # top-20 list
        pygame.draw.rect(self.surface, WOOD_LIGHT, (350, 80, 400, 300), border_radius = 15)
        pygame.draw.rect(self.surface, WOOD_DARK, (350, 80, 400, 300), width = 5, border_radius = 15)

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            # self.check_mouse_hover()
            # for event in pygame.event.get():
            #     self.handle_input(event)

            # self.on_loop()
            self.on_render()

            pygame.display.update()
            self._clock.tick(120)
        
        self.on_cleanup()


def on_render():
    draw_background(self)



pygame.quit()
sys.exit()