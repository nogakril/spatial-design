import pygame
import os

from Photo import Photo


def load_image(path, scale=None):
    if not os.path.exists(path):
        return None
    img = pygame.image.load(path)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


class GUIManager:
    def __init__(self, gallery_manager, logo_path="gallery/logo.png", buttons_controller=None,
                 camera_manager=None):
        self.gallery_manager = gallery_manager
        self.window_width, self.window_height = (None, None)
        self.logo_path = logo_path
        self.logo = None
        self.screen = None
        self.running = True
        self.buttonsController = buttons_controller
        self.camera = camera_manager
        self.clock = pygame.time.Clock()

    def start(self):
        pygame.init()
        info = pygame.display.Info()
        self.window_width, self.window_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode(( self.window_width, self.window_height)) #, pygame.FULLSCREEN)
        pygame.display.set_caption("Photo Gallery")

        self.logo = load_image(self.logo_path, (self.window_width * 0.2, self.window_height * 0.1))

        while self.running:
            self.handle_events()
            # Check for button events

            # buttons_input_event = self.buttonsController.get_input()
            # if buttons_input_event:
            #     self.process_buttons_input(buttons_input_event)
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

    def process_buttons_input(self, buttons_input_event):
        if buttons_input_event.get('joystick'):
            self.on_joystick_move(buttons_input_event['joystick'])
        if buttons_input_event.get('button'):
            self.on_button_press(buttons_input_event['button'])

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

            # Draw child indicator
            if photo.children:
                self.draw_child_indicator(True)
            else:
                self.draw_child_indicator(False)

    def draw_photo(self, path):
        if not os.path.exists(path):
            return
        photo_img = pygame.image.load(path)
        photo_img = self.scale_to_fit(photo_img)
        rect = photo_img.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(photo_img, rect)

    def scale_to_fit(self, image):
        iw, ih = image.get_size()
        scale = 0.5
        return pygame.transform.scale(image, (int(iw * scale), int(ih * scale)))

    def draw_child_indicator(self, has_children):
        color = (0, 255, 0) if has_children else (255, 0, 0)
        radius = 10
        pygame.draw.circle(self.screen, color, (self.window_width - 30, 30), radius)
