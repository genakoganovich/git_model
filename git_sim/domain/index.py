class Index:
    def __init__(self):
        self._files = {}

    def add(self, filename: str, content: str):
        self._files[filename] = content

    def snapshot(self) -> dict:
        return dict(self._files)

    def clear(self):
        self._files.clear()