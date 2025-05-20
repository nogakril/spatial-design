from arduino.ArduinoController import ArduinoController
from CameraManager import CameraManager
from GUIManager import GUIManager
from gallery.GalleryManager import GalleryManager

if __name__ == '__main__':
    gallery_manager = GalleryManager()
    camera_manager = CameraManager()
    # arduino_controller = ArduinoController()
    gui = GUIManager(gallery_manager=gallery_manager,
                     # arduino_controller=arduino_controller,
                     camera_manager=camera_manager
                     )
    gui.start()
