import os


class Path:
    def __init__(self):
        self.base_path = None
        self.base_path_has_been_set = False

    def set_base_path(self, path: str):
        if not self.base_path_has_been_set:
            self.base_path = path
            self.base_path_has_been_set = True
        else:
            raise Exception("Base path has already been set")

    def get_base_path(self) -> str:
        if self.base_path:
            return self.base_path
        else:
            raise Exception("Base path has not been set")

    def rel_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)


path = Path()
