import os
import shutil

import willowDb.utils.errorHandler as errorHandler
import willowDb.coreFunctions.table as table
import willowDb.coreFunctions.files as files


class Setup():
    def __init__(self, folderPath: str = None, errorConfig: str = None):
        if folderPath:
            self.folderPath = folderPath
            if self.folderPath[-1] != '/':
                self.folderPath = self.folderPath + '/'
        self.errorConfig = errorConfig
        if folderPath == None:
            currentFilePath = os.path.realpath(__file__)
            currentFilePathSplit = currentFilePath.split('/')
            self.baseFolder = '/'.join(currentFilePathSplit[:-1]) + '/tables/'
        else:
            self.baseFolder = self.folderPath
        self.errorHandler = errorHandler.ErrorHandler(self.errorConfig)

    def table(self, name: str, createPrimaryKey: bool = False):
        return table.TableClass(
            name=name,
            folderPath=self.baseFolder,
            errorHandler=self.errorHandler,
            createPrimaryKey=createPrimaryKey
        )
    
    def createTable(self, name: str, primaryKey: str):
        if not os.path.exists(self.baseFolder + name):
            os.makedirs(f"{self.baseFolder}{name}")
            os.makedirs(f"{self.baseFolder}{name}/records/")
            os.makedirs(f"{self.baseFolder}{name}/indexes/")
        else:
            return self.errorHandler.tableAlreadyExists(name, "CreateTable")
        indexConfig = files.Files(filePath=f"{self.baseFolder}{name}/indexes.willow", mode="w+", errorHandler=self.errorHandler)
        indexConfig.write({"default": {"primaryKey": primaryKey}})
        return {"willDbStatus": "success"}
    
    def listTables():
        if os.path.exists(self.baseFolder):
            allItems = os.listdir(self.baseFolder)
            justDirs = []
            for item in allItems:
                if os.path.isdir(self.baseFolder + item):
                    justDirs.append(item)
            return justDirs
        else:
            return []
            
    def deleteTable(self, name: str):
        tableFolder = self.baseFolder + name
        if os.path.exists(tableFolder):
            shutil.rmtree(tableFolder, ignore_errors=True)
        else:
            return self.errorHandler.noTable(name, "DeleteTable")
        return {"willDbStatus": "success"}
    