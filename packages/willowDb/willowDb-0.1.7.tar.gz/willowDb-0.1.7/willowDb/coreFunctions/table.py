import os

import willowDb.dbFunctions.delete as delete
import willowDb.dbFunctions.update as update
import willowDb.dbFunctions.insert as insert
import willowDb.dbFunctions.query as query
import willowDb.dbFunctions.createIndex as createIndex
import willowDb.dbFunctions.deleteIndex as deleteIndex
import willowDb.dbFunctions.scan as scan
import willowDb.coreFunctions.files as files


class TableClass():
        def __init__(self, name:str, folderPath:str, errorHandler: str, createPrimaryKey: bool = False):
            self.createPrimaryKey = createPrimaryKey
            self.errorHandler = errorHandler
            self.tableName = name
            self.tableFolder = None
            if folderPath == None:
                self.baseFolder = os.path.realpath(__file__) + "/tables/"
            else:
                self.baseFolder = folderPath
            if os.path.exists(f"{self.baseFolder}{self.tableName}"):
                self.tableFolder = f"{self.baseFolder}{ self.tableName}/"
                self.recordsFolder = self.tableFolder + 'records/'
                self.indexesFolder = self.tableFolder + 'indexes/'
            else:
                self.errorHandler.noTable(self.tableName, "Class Init")

        def scan(self, filter: str = None):
            scanClass = scan.ScanClass(errorHandler=self.errorHandler)
            return scanClass.scan(
                filter=filter,
                tableName=self.tableName,
                tableFolder=self.tableFolder,
                recordsFolder=self.recordsFolder
            )
                
        def query(self, primaryKey: str, indexName: str = "default"):
            queryClass = query.QueryClass(errorHandler=self.errorHandler)
            return queryClass.query(
                primaryKey=primaryKey,
                indexName=indexName,
                tableName=self.tableName,
                indexesFolder=self.indexesFolder,
                recordsFolder=self.recordsFolder,
                tableFolder=self.tableFolder
            )

        def delete(self, primaryKey: str):
            deleteClass = delete.DeleteClass(errorHandler=self.errorHandler)
            return deleteClass.delete(
                primaryKey=primaryKey,
                tableName=self.tableName,
                recordsFolder=self.recordsFolder,
                tableFolder=self.tableFolder
            )
            
        def update(self, record: dict, primaryKey: str = None):
            updateClass = update.UpdateClass(errorHandler=self.errorHandler)
            return updateClass.update(
                primaryKey=primaryKey,
                record=record,
                tableName=self.tableName,
                recordsFolder=self.recordsFolder,
                tableFolder=self.tableFolder
            )

        def insert(self, data: dict):
            insertClass = insert.InsertClass(errorHandler=self.errorHandler)
            return insertClass.insert(
                data=data,
                tableName=self.tableName,
                recordsFolder=self.recordsFolder,
                tableFolder=self.tableFolder,
                createPrimaryKey=self.createPrimaryKey
            )

        def createIndex(self, indexName: str, primaryKey: str):
            createIndexClass = createIndex.CreateIndexClass(errorHandler=self.errorHandler)
            return createIndexClass.createIndex(
                indexName=indexName,
                primaryKey=primaryKey,
                indexesFolder=self.indexesFolder,
                tableName=self.tableName,
                tableFolder=self.tableFolder,
                recordsFolder=self.recordsFolder,
            )
        
        def deleteIndex(self, indexName: str):
            deleteIndexClass = deleteIndex.DeleteIndexClass(errorHandler=self.errorHandler)
            return deleteIndexClass.deleteIndex(
                indexName=indexName,
                indexesFolder=self.indexesFolder,
            )
