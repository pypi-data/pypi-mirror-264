import os
import shutil

import willowDb.coreFunctions.files as files
import willowDb.utils.common as common


class DeleteIndexClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler
        self.common = common.Common()

    def deleteIndex(
            self,
            indexName: str,
            indexesFolder: str,
        ):
        indexFolderPath = f"{indexesFolder}{indexName}"
        if os.path.exists(indexFolderPath):
            shutil.rmtree(indexFolderPath, ignore_errors=True)
        