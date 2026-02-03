# ui.py
import pygame
from settings import *

class UIRenderer:
    def __init__(self, surface):
        self.surface = surface
        self.font_keyboard = pygame.font.SysFont(None, 36)
        self.font_special = pygame.font.SysFont(None, 18)

    def draw_grid(self, stop_animation_pos, bubble_finished):
        """draw grid"""
        guess_area = []
        # Vẽ các ô
        # Logic: range(start, stop, step)
        for y in range(20, 20 + 5 * 56 + 1, 56):
            for x in range(335, WIDTH - 384, 56):
                # Nếu đang có animation tại ô này thì bỏ qua (để vẽ bubble sau)
                if (stop_animation_pos and 
                    x + 25 == stop_animation_pos[0] and 
                    y + 25 == stop_animation_pos[1] and 
                    not bubble_finished):
                    guess_area.append((x, y, 50, 50)) # Vẫn thêm vào list để logic game dùng
                    continue
                
                pygame.draw.rect(self.surface, COLOR_GRID, (x, y, 50, 50), width=2, border_radius=7)
                guess_area.append((x, y, 50, 50))
        return guess_area

    def draw_keyboard(self):
        """draw keyboard and return click area"""
        click_area = []
        
        # Dòng 1
        start_x_1 = 273
        for i, char in enumerate(KEYBOARD_LAYOUT[0]):
            x = start_x_1 + i * (BUTTON_WIDTH + GAP_X)
            self._draw_key(char, x, KEYBOARD_Y_POS[0], click_area)

        # Dòng 2
        start_x_2 = 296
        for i, char in enumerate(KEYBOARD_LAYOUT[1]):
            x = start_x_2 + i * (BUTTON_WIDTH + GAP_X)
            self._draw_key(char, x, KEYBOARD_Y_POS[1], click_area)

        # Dòng 3
        start_x_3 = 342
        for i, char in enumerate(KEYBOARD_LAYOUT[2]):
            x = start_x_3 + i * (BUTTON_WIDTH + GAP_X)
            self._draw_key(char, x, KEYBOARD_Y_POS[2], click_area)

        # Nút ENTER
        self._draw_special_key("ENTER", 273, KEYBOARD_Y_POS[2], click_area)
        # Nút DELETE
        self._draw_special_key("DELETE", WIDTH - 335, KEYBOARD_Y_POS[2], click_area)

        return click_area

    def _draw_key(self, text, x, y, click_area_list):
        pygame.draw.rect(self.surface, COLOR_FILL, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=8)
        text_surf = self.font_keyboard.render(text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        self.surface.blit(text_surf, text_rect)
        click_area_list.append(pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT))

    def _draw_special_key(self, text, x, y, click_area_list):
        pygame.draw.rect(self.surface, COLOR_FILL, (x, y, SPECIAL_WIDTH, BUTTON_HEIGHT), border_radius=8)
        text_surf = self.font_special.render(text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=(x + SPECIAL_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        self.surface.blit(text_surf, text_rect)
        click_area_list.append(pygame.Rect(x, y, SPECIAL_WIDTH, BUTTON_HEIGHT))

    def draw_notification(self, text, start_time):
        """noti when wrong"""
        t = pygame.time.get_ticks() - start_time
        duration = 2000

        if t > duration:
            return False # Hết giờ hiển thị

        alpha = 255 - int((t / duration) * 255)
        font = pygame.font.SysFont(None, 46)
        surf = font.render(text, True, COLOR_WHITE)
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.surface.blit(surf, rect)
        return True