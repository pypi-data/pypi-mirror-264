import os

import willowDb.coreFunctions.files as files
import willowDb.utils.common as common


class CreateIndexClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler
        self.common = common.Common()

    def createIndex(
            self,
            indexName: str,
            primaryKey: str,
            indexesFolder: str,
            tableName: str,
            tableFolder: str,
            recordsFolder: str,
        ):
        indexFolderPath = f"{indexesFolder}{indexName}"
        if not os.path.exists(indexFolderPath):
            os.makedirs(indexFolderPath)
            indexRecordsFolder = f"{indexFolderPath}/records/"
            os.makedirs(indexRecordsFolder)
            indexConfigFilePath = f"{tableFolder}/indexes.willow"
            indexConfigFile = files.Files(filePath=indexConfigFilePath, mode="r+", errorHandler=self.errorHandler)
            indexConfig = indexConfigFile.read()
            indexData = {
                "primaryKey": primaryKey
            }
            indexConfig[indexName] = indexData
            indexConfigFile.write(data=indexConfig, close=True, truncate=True)

            if tableFolder:
                pages = self.common.getPages(tableFolder=tableFolder)
                for page in pages:
                    for file in page:
                        if file.endswith(".willow"):
                            recordFile = files.Files(filePath=f"{recordsFolder}{file}", mode="r", errorHandler=self.errorHandler)
                            recordFile = recordFile.read(close=True)
                            indexPrimaryKey = recordFile[primaryKey]
                            indexRecordFilePath = f"{indexRecordsFolder}{indexPrimaryKey}.willow"
                            if os.path.isfile(indexRecordFilePath):
                                indexRecordFile = files.Files(filePath=indexRecordFilePath, mode="r+", errorHandler=self.errorHandler)
                                indexRecord = indexRecordFile.read()
                                indexRecord.append(file)
                                indexRecordFile.write(data=indexRecord, close=True, truncate=True)
                            else:
                                indexRecordFile = files.Files(filePath=indexRecordFilePath, mode="w+", errorHandler=self.errorHandler)
                                indexRecordFile.write(data=[file], close=True)
            else:
                return self.errorHandler.noTable(tableName,"Scan")
        else:
            return self.errorHandler.indexAlreadyExists(indexName, "createIndex")

        