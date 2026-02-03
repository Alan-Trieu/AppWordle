# game.py
import pygame
import threading
import sys
from pygame.locals import *
from settings import *
from network import WordChecker
from ui import UIRenderer

class App:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self._clock = pygame.time.Clock()
        
        # Các thành phần logic
        self.network = WordChecker()
        self.ui = None # Sẽ khởi tạo trong on_init
        
        # Game State
        self._click_area = []
        self._guess_area = []
        self._texts = []
        self._current_guess = ""
        self._checking_word = False
        self._word_valid = None
        
        # Animation State
        self._scale = 1.0
        self._bubble_growing = False
        self._bubble_finished = True
        self._bubble_texts = []
        self._stop_animation = ()
        self._notification = None
        self._notification_start = 0

    # ---------------- Initialization ----------------
    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(
            SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        try:
            self._background_surface = pygame.image.load('Images/anime-style-earth.jpg').convert()
            self._background_surface = pygame.transform.scale(self._background_surface, SIZE)
        except Exception as e:
            print(f"Không tìm thấy ảnh nền: {e}")
            self._background_surface = pygame.Surface(SIZE)
            self._background_surface.fill((50, 50, 50))

        self.ui = UIRenderer(self._display_surface)
        self._running = True
        return True

    # ---------------- Logic xử lý từ ----------------
    def async_check_word(self, word):
        self._checking_word = True
        self._word_valid = self.network.check_word_api(word)
        self._checking_word = False

    def trigger_check_word(self):
        if len(self._current_guess) == 6 and not self._checking_word:
            threading.Thread(target=self.async_check_word, args=(self._current_guess,), daemon=True).start()

    # ---------------- Event Handling ----------------
    def handle_input(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_click(event)
            
        elif event.type == pygame.KEYDOWN:
            self.on_keyboard_press(event)

    def on_mouse_click(self, event):
        for rect in self._click_area:
            if rect.collidepoint(event.pos):
                # Xử lý tọa độ cứng (Có thể cải thiện sau, nhưng giữ logic cũ cho chuẩn)
                # Nút ENTER
                if rect[1] == 570 and rect[0] == 273:
                    self.trigger_check_word()
                # Nút DELETE
                elif rect[1] == 570 and rect[0] == WIDTH - 335:
                    if len(self._current_guess) > 0 and not self._checking_word:
                        self.remove_text()
                # Các nút chữ cái
                else:
                    self.process_virtual_keyboard_click(rect)
                break

    def process_virtual_keyboard_click(self, rect):
        char = ""
        # Logic tìm chữ dựa trên vị trí rect (Map ngược lại từ list trong settings)
        # Cách đơn giản nhất: Kiểm tra từng dòng
        if rect[1] == 450:
            idx = (rect[0] - 273) // 46
            if 0 <= idx < len(KEYBOARD_LAYOUT[0]): char = KEYBOARD_LAYOUT[0][idx]
        elif rect[1] == 510:
            idx = (rect[0] - 296) // 46
            if 0 <= idx < len(KEYBOARD_LAYOUT[1]): char = KEYBOARD_LAYOUT[1][idx]
        elif rect[1] == 570:
            idx = (rect[0] - 342) // 46
            if 0 <= idx < len(KEYBOARD_LAYOUT[2]): char = KEYBOARD_LAYOUT[2][idx]
            
        if char and len(self._current_guess) < 6:
            self.add_text(char)

    def on_keyboard_press(self, event):
        char = event.unicode.upper()
        if char.isalpha() and len(self._current_guess) < 6:
            self.add_text(char)
        elif event.key == pygame.K_RETURN:
            self.trigger_check_word()
        elif event.key == pygame.K_BACKSPACE and len(self._current_guess) > 0:
            self.remove_text()

    def check_mouse_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = any(rect.collidepoint(mouse_pos) for rect in self._click_area)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if is_hover else pygame.SYSTEM_CURSOR_ARROW)

    # ---------------- Text Management ----------------
    def add_text(self, text):
        self._bubble_texts.clear()
        self._bubble_growing = True
        self._bubble_finished = False
        
        idx = len(self._current_guess)
        if idx >= len(self._guess_area): return # Prevent overflow

        rect = self._guess_area[idx]
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(text, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        
        self._stop_animation = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
        self._bubble_texts.append((text, rect))
        self._texts.append((text_surface, text_rect, self._stop_animation))
        self._current_guess += text

    def remove_text(self):
        if len(self._current_guess) and len(self._texts):
            self._current_guess = self._current_guess[:-1]
            self._texts.pop()

    def show_notification(self, text):
        self._notification = text
        self._notification_start = pygame.time.get_ticks()

    # ---------------- Drawing & Loop ----------------
    def draw_bubble_animation(self):
        if self._bubble_finished: return
        
        self._scale += BUBBLE_SPEED * self._bubble_growing
        if self._scale >= MAX_SCALE:
            self._bubble_growing *= -1 
        
        if self._scale <= 1:
            self._bubble_finished = True
            self._scale = 1.0

        font_size = 36
        scaled_font_size = int(font_size * self._scale)
        font = pygame.font.SysFont(None, scaled_font_size)
        
        for text, rect in self._bubble_texts:
            text_surface = font.render(text, True, COLOR_WHITE)
            cx, cy = rect[0] + rect[2] // 2, rect[1] + rect[3] // 2
            text_rect = text_surface.get_rect(center=(cx, cy))
            
            # Vẽ viền ô phóng to
            w, h = rect[2] * self._scale, rect[3] * self._scale
            pygame.draw.rect(self._display_surface, COLOR_BLACK, 
                             (cx - w/2, cy - h/2, w, h), width=2, border_radius=7)
            self._display_surface.blit(text_surface, text_rect)

    def on_loop(self):
        if self._word_valid is not None:
            if self._word_valid:
                print("Valid word") # Logic game đúng ở đây
                # Reset hoặc chuyển dòng tiếp theo
            else:
                self.show_notification("Word not found")
            self._word_valid = None

    def on_render(self):
        self._display_surface.blit(self._background_surface, (0, 0))
        
        # UI Renderer trả về các vùng click và vùng ô chữ
        self._guess_area = self.ui.draw_grid(self._stop_animation, self._bubble_finished)
        self._click_area = self.ui.draw_keyboard()

        # Vẽ các chữ đã nhập (trừ chữ đang animation)
        for text_surface, text_rect, center_rect in self._texts:
            if (self._stop_animation and center_rect == self._stop_animation 
                and not self._bubble_finished):
                continue
            self._display_surface.blit(text_surface, text_rect)

        self.draw_bubble_animation()

        if self._notification:
            still_showing = self.ui.draw_notification(self._notification, self._notification_start)
            if not still_showing:
                self._notification = None

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self.check_mouse_hover()
            for event in pygame.event.get():
                self.handle_input(event)

            self.on_loop()
            self.on_render()

            pygame.display.update()
            self._clock.tick(120)
        
        self.on_cleanup()