import pygame
import os

from gallery.Photo import Photo


class GUIManager:
    def __init__(self, gallery_manager, logo_path="gallery/logo.png", arduino_controller=None,
                 camera_manager=None, led_controller=None):
        self.gallery_manager = gallery_manager
        self.window_width, self.window_height = (None, None)
        self.logo_path = logo_path
        self.logo = None
        self.screen = None
        self.running = True
        self.arduino_controller = arduino_controller
        self.camera = camera_manager
        self.leds = led_controller
        self.clock = pygame.time.Clock()

    def start(self):
        pygame.init()
        info = pygame.display.Info()
        self.window_width, self.window_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))  # , pygame.FULLSCREEN)
        pygame.display.set_caption("Photo Gallery")

        self.logo = self._load_image(self.logo_path, scale=(self.window_width * 0.2, self.window_height * 0.1))

        while self.running:
            self.handle_events()
            # Check for button events

            # arduino_input_event = self.arduino_controller.get_input()
            # if buttons_input_event:
            #     self.process_arduino_input(arduino_input_event)
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
                if event.key == pygame.K_SPACE:
                    self.on_button_press("SAVE")
                if event.key == pygame.K_CAPSLOCK:
                    self.on_button_press("CONNECT")
                if event.key == pygame.K_UP:
                    self.on_joystick_move('UP')
                if event.key == pygame.K_DOWN:
                    self.on_joystick_move('DOWN')
                if event.key == pygame.K_LEFT:
                    self.on_joystick_move('LEFT')
                if event.key == pygame.K_RIGHT:
                    self.on_joystick_move('RIGHT')

    def process_arduino_input(self, buttons_arduino_event):
        if buttons_arduino_event.get('joystick'):
            self.on_joystick_move(buttons_arduino_event['joystick'])
        if buttons_arduino_event.get('button'):
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
        elif button == 'CONNECT':
            path = self.camera.capture_photo()
            new_photo = Photo(file_path=path)
            self.gallery_manager.connect_new_child(new_photo)

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the logo
        if self.logo:
            self.screen.blit(self.logo, (10, 10))

        # Draw current photo
        photo = self.gallery_manager.get_current_photo()
        if photo:
            self.draw_photo(photo.file_path)

            # Draw arrows
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            check_methods = {
                'UP': self.gallery_manager.can_move_up,
                'DOWN': self.gallery_manager.can_move_down,
                'LEFT': self.gallery_manager.can_move_left_right,
                'RIGHT': self.gallery_manager.can_move_left_right
            }

            for direction in directions:
                if check_methods[direction]():
                    self.leds.turn_on_led(direction)
                    print(f"Light arrow {direction.lower()}")
                else:
                    self.leds.turn_off_led(direction)

    def draw_photo(self, path):
        if not os.path.exists(path):
            return
        photo_img = pygame.image.load(path)
        photo_img = self._scale_to_fit(photo_img)
        rect = photo_img.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(photo_img, rect)

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
