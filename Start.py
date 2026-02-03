import pygame
import sys
import json
import os

WIDTH = 1000
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

# Colors
BG_GREEN = (86, 133, 97)      
WOOD_LIGHT = (244, 186, 96)   
WOOD_DARK = (194, 130, 51)    
WOOD_DARKER = (139, 90, 30)   
PAPER_COLOR = (242, 230, 194) 
TEXT_COLOR = (255, 239, 213)  
TEXT_DARK = (50, 30, 10)
ICON_RED = (200, 50, 50)      

class GameMenu:
    def __init__(self):
        self._running = True
        self.surface = None
        self.size = SIZE
        self.font_title = None
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.buttons = []
        self.leaderboard = []
        self.scroll_offset = 0
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.leaderboard_file = os.path.join(self.current_dir, "leaderboard.txt")

    def on_init(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Wordle Game Menu")
        self._clock = pygame.time.Clock()
        
        # Fonts - sử dụng Segoe UI trực tiếp
        self.font_title = pygame.font.SysFont("segoe ui", 56)
        self.font_large = pygame.font.SysFont("segoe ui", 52)
        self.font_medium = pygame.font.SysFont("segoe ui", 28)
        self.font_small = pygame.font.SysFont("segoe ui", 20)
        
        # Define rectangular buttons
        self.buttons = [
            {"label": "NEW GAME", "pos": (30, 80), "size": (280, 100)},
            {"label": "RESUME", "pos": (30, 240), "size": (280, 100)},
            {"label": "QUIT", "pos": (30, 400), "size": (280, 100)},
        ]
        
        self.load_leaderboard()
        return True

    def load_leaderboard(self):
        """Load leaderboard from txt file"""
        print(f"\nDang tim file: {self.leaderboard_file}")
        
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.leaderboard = data
                    print(f"✓ Da tai {len(self.leaderboard)} nguoi tu file")
            except Exception as e:
                print(f"✗ Loi doc file: {e}")
                self.leaderboard = []
        else:
            print(f"✗ Khong tim thay file: {self.leaderboard_file}")
            self.leaderboard = []

    def draw_button(self, label, pos, size):
        """Draw a wooden button with label"""
        x, y = pos
        w, h = size
        
        # Draw main button
        pygame.draw.rect(self.surface, WOOD_LIGHT, (x, y, w, h), border_radius=15)
        # Draw border
        pygame.draw.rect(self.surface, WOOD_DARK, (x, y, w, h), width=6, border_radius=15)
        # Draw shadow
        pygame.draw.line(self.surface, WOOD_DARKER, (x + 10, y + h - 5), (x + w - 10, y + h - 5), 5)
        
        # Draw text
        text_surf = self.font_large.render(label, True, TEXT_DARK)
        text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
        self.surface.blit(text_surf, text_rect)

    def draw_scoreboard(self):
        """Draw the scoreboard/leaderboard area with scrolling"""
        x, y, w, h = 350, 60, 620, 580
        
        # Main panel (paper color)
        pygame.draw.rect(self.surface, PAPER_COLOR, (x, y, w, h), border_radius=20)
        pygame.draw.rect(self.surface, WOOD_DARK, (x, y, w, h), width=8, border_radius=20)
        
        # Header with background
        header_height = 60
        pygame.draw.rect(self.surface, WOOD_DARK, (x, y, w, header_height), border_radius=20)
        
        header_text = self.font_title.render("TOP 20 LEADERBOARD", True, TEXT_COLOR)
        header_rect = header_text.get_rect(center=(x + w // 2, y + header_height // 2))
        self.surface.blit(header_text, header_rect)
        
        # Column headers
        header_y = y + 75
        rank_text = self.font_small.render("Rank", True, TEXT_DARK)
        name_text = self.font_small.render("Player Name", True, TEXT_DARK)
        time_text = self.font_small.render("Avg Time (s)", True, TEXT_DARK)
        
        self.surface.blit(rank_text, (x + 20, header_y))
        self.surface.blit(name_text, (x + 80, header_y))
        self.surface.blit(time_text, (x + 420, header_y))
        
        # Divider line
        pygame.draw.line(self.surface, WOOD_DARK, (x + 20, header_y + 35), (x + w - 20, header_y + 35), 2)
        
        # Draw leaderboard items
        items_per_page = 7
        item_height = 60
        
        content_y = header_y + 50
        
        for i in range(items_per_page):
            leaderboard_index = i + self.scroll_offset
            
            if leaderboard_index >= len(self.leaderboard):
                break
            
            item_y = content_y + i * item_height
            player = self.leaderboard[leaderboard_index]
            
            # Rank - larger
            rank_num = self.font_medium.render(str(leaderboard_index + 1), True, TEXT_DARK)
            self.surface.blit(rank_num, (x + 25, item_y))
            
            # Player name
            player_name_text = player["name"][:25]
            player_name = self.font_medium.render(player_name_text, True, TEXT_DARK)
            self.surface.blit(player_name, (x + 80, item_y))
            
            # Average time
            time_str = f"{player['avg_time']:.1f}s"
            avg_time = self.font_medium.render(time_str, True, TEXT_DARK)
            self.surface.blit(avg_time, (x + 440, item_y))
        
        # Draw scroll hint
        if len(self.leaderboard) > items_per_page:
            scroll_text = f"Scroll: {self.scroll_offset + 1}-{min(self.scroll_offset + items_per_page, len(self.leaderboard))} / {len(self.leaderboard)}"
            scroll_info = self.font_small.render(scroll_text, True, TEXT_DARK)
            self.surface.blit(scroll_info, (x + 20, y + h - 35))

    def draw(self):
        """Main draw function"""
        self.surface.fill(BG_GREEN)
        
        for button in self.buttons:
            self.draw_button(button["label"], button["pos"], button["size"])
        
        self.draw_scoreboard()

    def on_render(self):
        self.draw()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.scroll_offset = max(0, self.scroll_offset - 1)
                    elif event.y < 0:
                        max_scroll = max(0, len(self.leaderboard) - 7)
                        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.scroll_offset = max(0, self.scroll_offset - 1)
                    elif event.key == pygame.K_DOWN:
                        max_scroll = max(0, len(self.leaderboard) - 7)
                        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

            self.on_render()
            self._clock.tick(60)
        
        self.on_cleanup()

if __name__ == "__main__":
    app = GameMenu()
    app.on_execute()