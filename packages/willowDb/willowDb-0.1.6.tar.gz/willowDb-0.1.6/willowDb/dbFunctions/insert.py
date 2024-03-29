import os
import uuid

import willowDb.coreFunctions.files as files


class InsertClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler

    def handleIndexMapping(self, data: str, indexConfig: list, tableFolder: str):
        defaultPrimaryKey = indexConfig["default"]["primaryKey"]
        for index in indexConfig:
            indexName = index
            primaryKey = indexConfig[index]["primaryKey"]
            if indexName != "default":
                if primaryKey in data:
                    indexValue = data[primaryKey]
                    defaultIndexValue = data[defaultPrimaryKey]
                    indexRecordFilePath = f"{tableFolder}indexes/{indexName}/records/{indexValue}.willow"
                    fileMode = "r+"
                    if not os.path.isfile(indexRecordFilePath):
                        fileMode = "w+"
                    indexRecordFile = files.Files(filePath=indexRecordFilePath, mode=fileMode, errorHandler=self.errorHandler)
                    if fileMode == "w+":
                        indexRecord = []
                    else:
                        indexRecord = indexRecordFile.read()
                    indexRecord.append(f"{defaultIndexValue}.willlow")
                    indexRecordFile.write(data=indexRecord, close=True, truncate=True)
                else:
                    return self.errorHandler.primaryKeyNotFound(primaryKey, "insert", indexName)
        return data

    def insert(
            self,
            data: str,
            tableName: str,
            recordsFolder: str,
            tableFolder: str,
            createPrimaryKey: str
        ):
        if tableFolder:
            indexConfifFilePath = f"{tableFolder}indexes.willow"
            if os.path.isfile(indexConfifFilePath):
                indexConfig = files.Files(filePath=indexConfifFilePath, mode="r", errorHandler=self.errorHandler).read(close=True)
                defaultPrimaryKey = indexConfig["default"]["primaryKey"]
                if defaultPrimaryKey not in data:
                    if createPrimaryKey:
                        data[defaultPrimaryKey] = str(uuid.uuid4())
                    else:
                        return self.errorHandler.primaryKeyNotFoundinRecord("insert")
                filePath = f"{recordsFolder}{data[defaultPrimaryKey]}.willow"
                if not os.path.isfile(filePath):
                    files.Files(filePath=filePath, mode="w+", errorHandler=self.errorHandler).write(data=data, close=True, truncate=True)
                else:
                    self.errorHandler.primaryKeyAlreadyUsed(tableName, "insert", data[defaultPrimaryKey])
                self.handleIndexMapping(data=data, indexConfig=indexConfig, tableFolder=tableFolder)
            else:
                return self.errorHandler.noIndexFile(tableName, "insert", "default")
            return data
        else:
            return self.errorHandler.noTable(tableName, "insert")