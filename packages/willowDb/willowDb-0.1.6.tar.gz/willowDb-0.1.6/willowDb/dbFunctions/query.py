import os

import willowDb.coreFunctions.files as files


class QueryClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler
        self.allRecords = []
        self.threadList = []

    def readRecordFile(self, filePath: str):
        record = files.Files(filePath=filePath, mode="r", errorHandler=self.errorHandler).read(close=True)
        self.allRecords.append(record)
        
    def query(
            self,
            primaryKey: str,
            indexName: str,
            tableName: str,
            indexesFolder: str,
            recordsFolder: str,
            tableFolder: str
        ):
        if indexName != "default":
            indexFilePath = f"{indexesFolder}{indexName}/records/{primaryKey}.willow"
            primaryKeys = files.Files(filePath=indexFilePath, mode="r", errorHandler=self.errorHandler).read(close=True)
        else:
            primaryKeys = [f"{primaryKey}.willow"]
        if tableFolder:
            for pk in primaryKeys:
                filePath = f"{recordsFolder}{pk}"
                if os.path.isfile(filePath):
                    self.readRecordFile(filePath=filePath)     
            if len(self.allRecords) == 0:
                return None
            if len(self.allRecords) == 1:
                return self.allRecords[0]
            else:
                return self.allRecords
        else:
            return self.errorHandler.noTable(tableName, "Query")