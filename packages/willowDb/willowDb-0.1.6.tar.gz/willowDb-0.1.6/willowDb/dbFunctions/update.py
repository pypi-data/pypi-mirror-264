import os

import willowDb.coreFunctions.files as files


class UpdateClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler

    def handleIndexMapping(self, record: dict, primaryKey: str, tableFolder: str, recordOnFile: dict, indexConfig: dict):
        for index in indexConfig:
            indexName = index
            if indexName != "default":
                indexPrimaryKey = indexConfig[index]["primaryKey"]
                if indexPrimaryKey in record and recordOnFile[indexPrimaryKey] != record[indexPrimaryKey]:
                    if indexPrimaryKey in recordOnFile:
                        indexRecordOnFilePath = f"{tableFolder}indexes/{indexName}/records/{recordOnFile[indexPrimaryKey]}.willow"
                        if os.path.isfile(indexRecordOnFilePath):
                            indexRecordOnFile = files.Files(filePath=indexRecordOnFilePath, mode="r+", errorHandler=self.errorHandler)
                            indexRecordInDb = indexRecordOnFile.read()
                            del indexRecordInDb[indexRecordInDb.index(f"{primaryKey}.willow")]
                            indexRecordOnFile.write(data=indexRecordInDb, close=True, truncate=True)
                            if len(indexRecordInDb) == 0:
                                os.remove(indexRecordOnFilePath)
                        else:
                            return self.errorHandler.fileDoesNotExist(indexRecordOnFilePath, "update")
                        indexRecordFilePath = f"{tableFolder}indexes/{indexName}/records/{record[indexPrimaryKey]}.willow"
                        fileMode = "r+"
                        if not os.path.isfile(indexRecordFilePath):
                            fileMode = "w+"
                        indexRecordFile = files.Files(filePath=indexRecordFilePath, mode=fileMode, errorHandler=self.errorHandler)
                        if fileMode == "w+":
                            indexRecord = []
                        else:
                            indexRecord = indexRecordFile.read()
                        indexRecord.append(f"{primaryKey}.willow")
                        indexRecordFile.write(data=indexRecord, close=True, truncate=True)
    
    def update(self, primaryKey: str, record: str, tableName: str, recordsFolder: str, tableFolder: str):
        indexConfig = files.Files(filePath=f"{tableFolder}indexes.willow", mode="r", errorHandler=self.errorHandler).read(close=True)
        if primaryKey is None:
            if indexConfig["default"]["primaryKey"] in record:
                primaryKey = record[indexConfig["default"]["primaryKey"]]
            else:
                self.errorHandler.primaryKeyNotFoundinRecord("update")
        if tableFolder:
            filePath = f"{recordsFolder}{primaryKey}.willow"
            if os.path.isfile(filePath):
                recordFile = files.Files(filePath=filePath, mode="r+", errorHandler=self.errorHandler)
                recordOnFile = recordFile.read(close=False)
                recordOnFileOriginal = {**recordOnFile}
                for key in record:
                    if key != primaryKey:
                        recordOnFile[key] = record[key]
                recordFile.write(data=recordOnFile, close=True, truncate=True)
                self.handleIndexMapping(record=record, primaryKey=primaryKey, tableFolder=tableFolder, recordOnFile=recordOnFileOriginal, indexConfig=indexConfig)
                return {"willDbStatus": "success"}
            else:
                self.errorHandler.primaryKeyNotFound(tableName, "update")
        else:
            return self.errorHandler.noTable(tableName, "update")