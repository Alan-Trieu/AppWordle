import pygame
import sys

# Giả lập settings nếu bạn chưa có file settings.py
# Nếu có rồi thì giữ nguyên dòng import settings của bạn và xóa 3 dòng dưới
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

BG_GREEN = (86, 133, 97)      
WOOD_LIGHT = (244, 186, 96)   
WOOD_DARK = (194, 130, 51)     
PAPER_COLOR = (242, 230, 194) 
TEXT_COLOR = (255, 239, 213)  
ICON_RED = (200, 50, 50)      

class GameMenu: # Đổi tên class cho hợp lý hơn
    def __init__(self):
        self._running = True
        self.surface = None
        self.size = SIZE

    def on_init(self):
        pygame.init()
        # Khởi tạo màn hình chính tại đây
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Wooden Game Menu")
        self._clock = pygame.time.Clock()
        return True

    def draw(self):
        # 1. Vẽ màu nền
        self.surface.fill(BG_GREEN)

        # 2. Vẽ Rect buttons (Các nút hình chữ nhật bên trái)
        for y in range(100, 301, 100):
            pygame.draw.rect(self.surface, WOOD_LIGHT, (50, y, 220, 80), border_radius=5)
            # Vẽ viền cho đẹp hơn
            pygame.draw.rect(self.surface, WOOD_DARK, (50, y, 220, 80), width=3, border_radius=5)

        # 3. Vẽ Circle buttons (Các nút tròn bên dưới)
        for x in range(150, WIDTH - 150 + 1, 100): # Khoảng cách bước nhảy nên lớn hơn bán kính
            # SỬA LỖI: rect.center không có ngoặc ()
            center_x = x
            center_y = 500
            radius = 30 # Đặt bán kính cố định
            
            # SỬA LỖI: Thêm tham số tâm (center_x, center_y)
            pygame.draw.circle(self.surface, WOOD_LIGHT, (center_x, center_y), radius)
            pygame.draw.circle(self.surface, WOOD_DARK, (center_x, center_y), radius, width=3)

        # 4. Vẽ Top-20 list (Bảng bên phải)
        pygame.draw.rect(self.surface, PAPER_COLOR, (350, 80, 400, 300), border_radius=15) # Đổi thành màu giấy
        pygame.draw.rect(self.surface, WOOD_DARK, (350, 80, 400, 300), width=5, border_radius=15)

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
            # SỬA LỖI: Phải xử lý sự kiện, nếu không window sẽ bị treo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self.on_render()
            self._clock.tick(120) # 60 FPS là đủ cho menu
        
        self.on_cleanup()

# --- PHẦN QUAN TRỌNG NHẤT ---
# Phải kiểm tra name == main và gọi class chạy
if __name__ == "__main__":
    app = GameMenu()
    app.on_execute()