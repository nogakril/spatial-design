import os
from datetime import datetime

import cv2


class CameraManager:
    def __init__(self, save_dir: str = "gallery/images"):
        self.save_dir = save_dir
        self.cam_index = 0

    def capture_photo(self) -> str:
        cap = cv2.VideoCapture(self.cam_index)

        if not cap.isOpened():
            raise IOError("Cannot open camera")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise IOError("Failed to capture image")

        # Save image with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, frame)

        print(f"Saved photo: {filepath}")
        return filepath

