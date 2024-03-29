import os
import math

class Common():                          
    def getPages(self, tableFolder: str):
        pages = []
        records = os.listdir(f"{tableFolder}records")
        recordsList = list(records)
        pageAmount = math.ceil(len(recordsList) / 1000)
        for i in range(0, pageAmount):
            page = recordsList[i * 1000: (i + 1) * 1000]
            pages.append(page)
        return pages