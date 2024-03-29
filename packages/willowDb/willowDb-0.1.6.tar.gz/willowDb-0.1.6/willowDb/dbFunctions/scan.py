import willowDb.coreFunctions.files as files
import willowDb.coreFunctions.filter as filter
import willowDb.utils.common as common


class ScanClass():
    def __init__(self, errorHandler: str):
        self.errorHandler = errorHandler
        self.filter = filter.Filter()
        self.common = common.Common()
        self.filterResults = []

    def readFile(self, filePath: str, pageRecords: list):
        record = files.Files(filePath=filePath, mode="r", errorHandler=self.errorHandler).read(close=True)
        pageRecords.append(record)

    def getPageData(self, page: list, recordsFolder: str, filter: str = None):
        pageRecords = []
        for file in page:
            if file.endswith(".willow"):
                filePath = f"{recordsFolder}{file}"
                record = files.Files(filePath=filePath, mode="r", errorHandler=self.errorHandler).read(close=True)
                pageRecords.append(record)
        if filter:
            results = self.filter.filter(pageRecords, filter)
            self.filterResults.extend(results)
        else:
            self.filterResults.extend(pageRecords)

    def scan(self, filter: str, tableName: str, tableFolder: str, recordsFolder: str):
        if tableFolder:
            pages = self.common.getPages(tableFolder=tableFolder)
            for page in pages:
                self.getPageData(page, recordsFolder, filter)
            if self.filterResults != []:
                return self.filterResults
            else:
                return None
        else:
            return self.errorHandler.noTable(tableName,"Scan")