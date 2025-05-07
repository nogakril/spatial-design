from ButtonsController import ButtonsController
from CameraManager import CameraManager
from GUIManager import GUIManager
from GalleryManager import GalleryManager

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gallery_manager = GalleryManager()
    camera_manager = CameraManager()
    buttons_controller = ButtonsController()
    gui = GUIManager(gallery_manager=gallery_manager,
                     buttons_controller=buttons_controller,
                     camera_manager=camera_manager)
    gui.start()
