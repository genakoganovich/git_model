from copy import deepcopy
import uuid


class Commit:
    def __init__(self, snapshot: dict, parent=None):
        self.id = str(uuid.uuid4())
        self.snapshot = deepcopy(snapshot)
        self.parent = parent