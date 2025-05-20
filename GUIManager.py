import time

import pygame
import os

from gallery.Photo import Photo

BLACK = (22, 22, 22)
YELLOW = (228, 255, 107)
PURPLE = (181, 186, 255)
BG_PATH = "gallery/background.png"
BG_NO_SIBLINGS_PATH = "gallery/background_no_siblings.png"
BG_NO_PARENT_NO_CHILDREN_PATH = "gallery/background_no_parent_no_children.png"
BG_NO_CHILDREN_PATH = "gallery/background_no_children.png"
BG_NO_PARENT_PATH = "gallery/background_no_parent.png"
INSTRUCTIONS_PATH = "gallery/instructions.png"
IDLE_TIMEOUT_SECONDS = 60


class GUIManager:
    def __init__(self, gallery_manager, arduino_controller=None, camera_manager=None):
        self.gallery_manager = gallery_manager
        self.window_width, self.window_height = (None, None)

        # bg
        self.background = None
        self.background_no_siblings = None
        self.background_no_children = None
        self.background_no_parent_no_children = None
        self.background_no_parent = None

        self.instructions = None
        self.screen = None
        self.running = True
        self.arduino_controller = arduino_controller
        self.camera = camera_manager
        self.clock = pygame.time.Clock()
        self.last_interaction_time = time.time()
        self.showing_instructions = True

    def start(self):
        pygame.init()
        info = pygame.display.Info()
        self.window_width, self.window_height = info.current_w, info.current_h
        # self.window_width, self.window_height = 1280, 720
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Labör Archive")

        # Load images
        self.background = self._load_image(BG_PATH, scale=(self.window_width, self.window_height))
        self.background_no_siblings = self._load_image(BG_NO_SIBLINGS_PATH,
                                                       scale=(self.window_width, self.window_height))
        self.background_no_parent_no_children = self._load_image(BG_NO_PARENT_NO_CHILDREN_PATH,
                                                                 scale=(self.window_width, self.window_height))
        self.background_no_children = self._load_image(BG_NO_CHILDREN_PATH,
                                                       scale=(self.window_width, self.window_height))
        self.background_no_parent = self._load_image(BG_NO_PARENT_PATH,
                                                     scale=(self.window_width, self.window_height))
        self.instructions = self._load_image(INSTRUCTIONS_PATH, scale=(self.window_width, self.window_height))

        while self.running:
            self.handle_events()
            # Check for button events

            if self.arduino_controller:
                arduino_input_event = self.arduino_controller.get_input()
            else:
                arduino_input_event = None

            if arduino_input_event:
                print(arduino_input_event)
                self.process_arduino_input(arduino_input_event)

            if self.showing_instructions:
                self.screen.blit(self.instructions, (0, 0))
            else:
                self.render()
            pygame.display.flip()
            self.clock.tick(30)

            if not self.showing_instructions and (time.time() - self.last_interaction_time > IDLE_TIMEOUT_SECONDS):
                self.showing_instructions = True

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
                #     self.on_button_press("COMMENT")
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
        self.last_interaction_time = time.time()
        if self.showing_instructions:
            self.showing_instructions = False

        if direction == 'UP':
            self.gallery_manager.move_up()
        elif direction == 'DOWN':
            self.gallery_manager.move_down()
        elif direction == 'LEFT':
            self.gallery_manager.move_left()
        elif direction == 'RIGHT':
            self.gallery_manager.move_right()

    def on_button_press(self, button: str):
        self.last_interaction_time = time.time()
        if self.showing_instructions:
            self.showing_instructions = False

        if button == 'SAVE':
            path = self.camera.capture_photo()
            new_photo = Photo(file_path=path)
            self.gallery_manager.add_root_photo(new_photo)
            self._flash_message("Photo Saved", color=YELLOW)
        elif button == 'COMMENT':
            path = self.camera.capture_photo()
            new_photo = Photo(file_path=path)
            self.gallery_manager.connect_new_child(new_photo)
            self._flash_message("Photo Connected", color=PURPLE)

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw current photo
        photo = self.gallery_manager.get_current_photo()
        prev_photo = self.gallery_manager.get_previous_photo()
        next_photo = self.gallery_manager.get_next_photo()
        no_parent = not photo.parent

        # Draw background
        if not prev_photo and not next_photo:
            self.screen.blit(self.background_no_siblings, (0, 0))
        elif len(photo.children) == 0:
            if no_parent:
                self.screen.blit(self.background_no_parent_no_children, (0, 0))
            else:
                self.screen.blit(self.background_no_children, (0, 0))
        elif no_parent:
            self.screen.blit(self.background_no_parent, (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))

        # Draw current photo
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

        if prev_photo and next_photo:
            self.draw_photo(prev_photo.file_path, x=-34, y=308, img_width=159, img_height=111)
            self.draw_photo(next_photo.file_path, x=1180, y=298, img_width=190, img_height=140)

    def draw_photo(self, path, x=450, y=247, img_width=412, img_height=275):
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

    def _draw_text(self, screen, text, size=12, color=YELLOW, x=400, y=98, font_name="menlo"):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        padding = 2
        text_rect = text_surface.get_rect()
        box_rect = pygame.Rect(x, y, text_rect.width + 2 * padding, text_rect.height + 2 * padding)
        pygame.draw.rect(screen, BLACK, box_rect)
        screen.blit(text_surface, (box_rect.x + padding, box_rect.y + padding))

    def _flash_message(self, message, bg_color=BLACK, color=YELLOW, duration=2):
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill(bg_color)
        self.screen.blit(overlay, (0, 0))
        self._draw_text(self.screen, message, color=color, size=50, x=400, y=200)
        pygame.display.flip()
        time.sleep(duration)
