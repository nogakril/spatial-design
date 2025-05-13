import pygame
import os

from gallery.Photo import Photo

os.environ['SDL_VIDEO_WINDOW_POS'] = "1920,0"
BLACK = (22, 22, 22)
YELLOW = (228, 255, 107)

class GUIManager:
    def __init__(self, gallery_manager, logo_path="gallery/background.png", arduino_controller=None,
                 camera_manager=None):
        self.gallery_manager = gallery_manager
        self.window_width, self.window_height = (None, None)
        self.logo_path = logo_path
        self.background = None
        self.screen = None
        self.running = True
        self.arduino_controller = arduino_controller
        self.camera = camera_manager
        self.clock = pygame.time.Clock()

    def start(self):
        pygame.init()
        info = pygame.display.Info()
        self.window_width, self.window_height = info.current_w, info.current_h ## 1512x982
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Labör Archive")

        self.background = self._load_image(self.logo_path, scale=(self.window_width, self.window_height))

        while self.running:
            self.handle_events()
            # Check for button events

            if self.arduino_controller:
                arduino_input_event = self.arduino_controller.get_input()
            else:
                arduino_input_event = None

            if arduino_input_event:
                self.process_arduino_input(arduino_input_event)
            self.render()
            pygame.display.flip()
            self.clock.tick(30)

        self.gallery_manager.save_structure()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC to quit
                    self.running = False

                # Remove when joystick is implemented
                # if event.key == pygame.K_SPACE:
                #     self.on_button_press("SAVE")
                # if event.key == pygame.K_CAPSLOCK:
                #     self.on_button_press("CONNECT")
                # if event.key == pygame.K_UP:
                #     self.on_joystick_move('UP')
                # if event.key == pygame.K_DOWN:
                #     self.on_joystick_move('DOWN')
                # if event.key == pygame.K_LEFT:
                #     self.on_joystick_move('LEFT')
                # if event.key == pygame.K_RIGHT:
                #     self.on_joystick_move('RIGHT')

    def process_arduino_input(self, buttons_arduino_event):
        if buttons_arduino_event.get('joystick'):
            self.on_joystick_move(buttons_arduino_event['joystick'])
        if buttons_arduino_event.get('button'):
            print(f"Button pressed: {buttons_arduino_event['button']}")
            self.on_button_press(buttons_arduino_event['button'])

    def on_joystick_move(self, direction: str):
        if direction == 'UP':
            self.gallery_manager.move_up()
        elif direction == 'DOWN':
            self.gallery_manager.move_down()
        elif direction == 'LEFT':
            self.gallery_manager.move_left()
        elif direction == 'RIGHT':
            self.gallery_manager.move_right()

    def on_button_press(self, button: str):
        if button == 'SAVE':
            path = self.camera.capture_photo()
            new_photo = Photo(file_path=path)
            self.gallery_manager.add_root_photo(new_photo)
        elif button == 'COMMENT':
            path = self.camera.capture_photo()
            new_photo = Photo(file_path=path)
            self.gallery_manager.connect_new_child(new_photo)

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the logo
        if self.background:
            self.screen.blit(self.background, (0, 0))

        # Draw current photo
        photo = self.gallery_manager.get_current_photo()
        prev_photo = self.gallery_manager.get_previous_photo()
        next_photo = self.gallery_manager.get_next_photo()

        if photo:
            self.draw_photo(photo.file_path)
            self._draw_text(self.screen, f"{photo.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

            # Draw arrows
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            check_methods = {
                'UP': self.gallery_manager.can_move_up,
                'DOWN': self.gallery_manager.can_move_down,
                'LEFT': self.gallery_manager.can_move_left_right,
                'RIGHT': self.gallery_manager.can_move_left_right
            }

            directions = [direction for direction in directions if check_methods[direction]()]
            if directions and self.arduino_controller:
                self.arduino_controller.send_led_states(directions)
        if prev_photo:
            self.draw_photo(prev_photo.file_path, x=-85, y=421, img_width=235, img_height=150)
        if next_photo:
            self.draw_photo(next_photo.file_path, x=1385, y=420, img_width=235, img_height=175)

    def draw_photo(self, path, x=550, y=350, img_width=470, img_height=350):
        if not os.path.exists(path):
            return
        photo_img = pygame.image.load(path)
        img1 = pygame.transform.scale(photo_img, (img_width, img_height))
        rect1 = pygame.Rect(x, y, x + img_width, y + img_height)
        self.screen.blit(img1, rect1)

    def _scale_to_fit(self, image):
        iw, ih = image.get_size()
        scale = 0.5
        return pygame.transform.scale(image, (int(iw * scale), int(ih * scale)))

    def _load_image(self, path, scale=None):
        if not os.path.exists(path):
            return None
        img = pygame.image.load(path)
        if scale:
            img = pygame.transform.scale(img, scale)
        return img

    def _draw_text(self, screen, text):
        font = pygame.font.SysFont("Arial", 16)
        text_surface = font.render(text, True, YELLOW)
        padding = 2
        text_rect = text_surface.get_rect()
        box_rect = pygame.Rect(460, 135, text_rect.width + 2 * padding, text_rect.height + 2 * padding)
        pygame.draw.rect(screen, BLACK, box_rect)
        screen.blit(text_surface, (box_rect.x + padding, box_rect.y + padding))