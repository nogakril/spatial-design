import json
import os

from Photo import Photo


class GalleryManager:
    def __init__(self, storage_path: str = "gallery/gallery.json"):
        self.root_photos = []
        self.current_photo = None
        self.current_sibling_index = 0
        self.storage_path = storage_path

        self._ensure_storage_dir()
        self.load_structure()

    def _ensure_storage_dir(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def add_root_photo(self, photo: Photo):
        self.root_photos.append(photo)
        self.current_photo = photo
        self.current_sibling_index = len(self.root_photos) - 1

    def connect_new_child(self, new_photo: Photo):
        new_photo.parent = self.current_photo
        self.current_photo.add_child(new_photo)
        self.current_photo = new_photo
        self.current_sibling_index = 0

    def move_up(self):
        if self.current_photo.parent:
            self.current_photo = self.current_photo.parent
            self.current_sibling_index = (
                self.current_photo.parent.children.index(self.current_photo)
                if self.current_photo.parent else 0
            )

    def move_down(self):
        if self.current_photo.children:
            self.current_photo = self.current_photo.children[0]
            self.current_sibling_index = 0

    def move_left(self):
        siblings = (
            self.current_photo.parent.children
            if self.current_photo.parent
            else self.root_photos
        )
        if self.current_sibling_index > 0:
            self.current_sibling_index -= 1
            self.current_photo = siblings[self.current_sibling_index]

    def move_right(self):
        siblings = (
            self.current_photo.parent.children
            if self.current_photo.parent
            else self.root_photos
        )
        if self.current_sibling_index < len(siblings) - 1:
            self.current_sibling_index += 1
            self.current_photo = siblings[self.current_sibling_index]

    def get_current_photo(self) -> Photo:
        return self.current_photo

    def save_structure(self):
        data = [photo.to_dict() for photo in self.root_photos]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        print("Gallery structure saved.")

    def load_structure(self):
        if not os.path.exists(self.storage_path):
            print("No gallery found. Starting fresh.")
            return
        with open(self.storage_path) as f:
            data = json.load(f)
        self.root_photos = [Photo.from_dict(d) for d in data]
        if self.root_photos:
            self.current_photo = self.root_photos[0]
            self.current_sibling_index = 0
        print("Gallery structure loaded.")
