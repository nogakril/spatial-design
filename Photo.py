import uuid
from datetime import datetime


class Photo:
    def __init__(self, file_path: str, parent: 'Photo' = None):
        self.id = str(uuid.uuid4())  # Unique identifier
        self.file_path = file_path
        self.parent = parent
        self.children = []
        self.timestamp = datetime.now()

    def add_child(self, child: 'Photo'):
        self.children.append(child)

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "timestamp": self.timestamp.isoformat(),
            "children": [child.to_dict() for child in self.children]
        }

    @classmethod
    def from_dict(cls, data, parent=None):
        photo = cls(file_path=data["file_path"], parent=parent)
        photo.id = data["id"]
        photo.timestamp = datetime.fromisoformat(data["timestamp"])
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data, parent=photo)
            photo.children.append(child)
        return photo

    def __repr__(self):
        return f"<Photo {self.id} | {self.file_path} | {self.timestamp.isoformat()}>"
