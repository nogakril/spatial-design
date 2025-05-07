from ButtonsController import ButtonsController
from CameraManager import CameraManager
from GUIManager import GUIManager
from gallery.GalleryManager import GalleryManager
from LEDController import LEDController

if __name__ == '__main__':
    gallery_manager = GalleryManager()
    camera_manager = CameraManager()
    buttons_controller = ButtonsController()
    led_controller = LEDController()
    gui = GUIManager(gallery_manager=gallery_manager,
                     buttons_controller=buttons_controller,
                     camera_manager=camera_manager,
                     led_controller=led_controller)
    gui.start()
