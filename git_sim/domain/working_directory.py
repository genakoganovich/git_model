class WorkingDirectory:
    def __init__(self):
        self._files = {}

    def write(self, filename: str, content: str):
        self._files[filename] = content

    def read(self, filename: str) -> str:
        return self._files[filename]

    def snapshot(self) -> dict:
        return dict(self._files)