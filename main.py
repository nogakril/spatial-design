from arduino.ArduinoInputController import ArduinoInputController
from CameraManager import CameraManager
from GUIManager import GUIManager
from gallery.GalleryManager import GalleryManager

if __name__ == '__main__':
    gallery_manager = GalleryManager()
    camera_manager = CameraManager()
    arduino_controller = ArduinoInputController()
    gui = GUIManager(gallery_manager=gallery_manager,
                     arduino_controller=arduino_controller,
                     camera_manager=camera_manager
                     )
    gui.start()
