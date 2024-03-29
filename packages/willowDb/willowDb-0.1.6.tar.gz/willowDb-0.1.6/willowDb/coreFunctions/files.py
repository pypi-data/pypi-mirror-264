import json


class Files():
    def __init__(self, filePath: str, mode: str, errorHandler: str):
        self.errorHandler = errorHandler
        try:
            self.file = open(filePath, mode)
        except Exception as e:
            return self.errorHandler.fileDoesNotExist(filePath, "openFile")

    def read(self, close: bool = False):
        data = json.loads(self.file.read())
        if close:
            self.file.close()
        return data

    def write(self, data: dict, close: bool = False, truncate: bool = False):
        if truncate:
            self.file.seek(0)
            self.file.truncate()
        self.file.write(json.dumps(data))
        if close:
            self.file.close()
        return True