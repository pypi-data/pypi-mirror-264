import willowDb.utils.errors as errors
import willowDb.utils.logger as logger


class ErrorHandler():
    def __init__(self, errorConfig):
        self.willowDbException = errors.WillowDbException()
        self.errorConfig = errorConfig
        self.errorMapping = {
            "noTable": self.willowDbException.NoTableFound,
            "tableAlreadyExists": self.willowDbException.TableAlreadyExists,
            "primaryKeyNotFound": self.willowDbException.PrimaryKeyNotFound,
            "noIndexFile": self.willowDbException.NoIndexFile,
            "fileDoesNotExist": self.willowDbException.FileDoesNotExist,
            "primaryKeyAlreadyUsed": self.willowDbException.PrimaryKeyAlreadyUsed,
        }

    def handleError(self, function, message, errorType):
        if self.errorConfig == "log" or self.errorConfig == "both":
            thisLogger = logger.Logger(function, "INFO")
            thisLogger.error(message)
        if self.errorConfig == "raise" or self.errorConfig == "both":
            raise self.errorMapping[errorType](message)
        return {"willDbStatus": "error", "message": message}

    def noTable(self, tableName, function):
        return self.handleError(
            function,
            f"Table {tableName} does not exist please use willowDb.createTable('{tableName}') to create it or use the web interface to create it",
            "noTable",
        )
    
    def tableAlreadyExists(self, tableName, function):
        return self.handleError(
            function,
            f"Table {tableName} already exists",
            "tableAlreadyExists"
        )
    
    def primaryKeyNotFound(self, tableName, function, indexName="default"):
        self.handleError(
            function,
            f"Primary key not found in table {tableName} for index {indexName}",
            "primaryKeyNotFound"
        )

    def primaryKeyNotFoundinRecord(self, function):
        self.handleError(
            function,
            f"Primary key not found in update record please supply a primary key in the record object or add the primaryKey argument to the update function",
            "primaryKeyNotFoundInRecord"
        )

    def primaryKeyAlreadyUsed(self, tableName, function, primaryKey):
        self.handleError(
            function,
            f"Primary key {primaryKey} already used in table {tableName}",
            "primaryKeyAlreadyUsed"
        )

    def noIndexFile(self, tableName, function, indexName):
        self.handleError(
            function,
            f"Index file for index {indexName} not found for table {tableName}",
            "noIndexFile"
        )

    def fileDoesNotExist(self, filePath, function):
        self.handleError(
            function,
            f"File {filePath} does not exist",
            "fileDoesNotExist"
        )

    def indexAlreadyExists(self, indexName, function):
        self.handleError(
            function,
            f"Index {indexName} already exists",
            "indexAlreadyExists"
        )