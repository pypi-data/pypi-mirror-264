import os

import willowDb.coreFunctions.files as files

class DeleteClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler


    def handleIndexMapping(self, data: dict, primaryKey: str, indexConfig: list, tableFolder: str):
        for index in indexConfig:
            indexName = index
            indexPrimaryKey = indexConfig[index]["primaryKey"]
            if indexName != "default":
                indexRecordFilePath = f"{tableFolder}indexes/{indexName}/records/{data[indexPrimaryKey]}.willow"
                if os.path.isfile(indexRecordFilePath):
                    indexRecordFile = files.Files(filePath=indexRecordFilePath, mode="r+", errorHandler=self.errorHandler)
                    indexRecord = indexRecordFile.read()
                    del indexRecord[indexRecord.index(f"{primaryKey}.willow")]
                    indexRecordFile.write(data=indexRecord, close=True, truncate=True)
                    if len(indexRecord) == 0:
                        os.remove(indexRecordFilePath)
                else:
                    return self.errorHandler.fileDoesNotExist(indexRecordFilePath, "insert")
    def delete(
            self,
            primaryKey: str,
            tableName: str,
            recordsFolder: str,
            tableFolder: str):
        filePath = f"{recordsFolder}{primaryKey}.willow"
        record = files.Files(filePath=filePath, mode="r", errorHandler=self.errorHandler).read(close=True)
        if tableFolder:
            filePath = f"{recordsFolder}{primaryKey}.willow"
            if os.path.isfile(filePath):
                os.remove(filePath)
            else:
                self.errorHandler.primaryKeyNotFound(tableName, "delete")
            indexConfifFilePath = f"{tableFolder}indexes.willow"
            indexConfig = files.Files(filePath=indexConfifFilePath, mode="r", errorHandler=self.errorHandler).read(close=True)
            self.handleIndexMapping(data=record, primaryKey=primaryKey, indexConfig=indexConfig, tableFolder=tableFolder)
        else:
            return self.errorHandler.noTable(tableName, "delete")