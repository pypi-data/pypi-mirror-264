class Filter():
    def __init__(self):
        self.operations = ['==', '>', '<', '!=', '>=', '<=', 'contains', 'not contains', 'startsWith', 'endsWith']

    def search(self, string, subString):
        indexes = []
        foundAll = True
        currentIndex = -1
        while foundAll:
            index = string[currentIndex+1:].find(subString)
            currentIndex = index + currentIndex + 1
            if index == -1:
                foundAll = False
            else:
                indexes.append(currentIndex)
        return indexes

    def getIndexOfKeys(self, filter, index, lastIndex):
        index += lastIndex
        combinedIndex = index
        rawKey = filter[lastIndex:combinedIndex]
        if rawKey[-1] == " ":
            rawKey = rawKey[:-1]
            combinedIndex -= 1
        allSpaces = self.search(rawKey, " ")
        startOfKey = lastIndex
        endOfKey = combinedIndex
        
        if len(allSpaces) != 0:
            startOfKey = startOfKey + allSpaces[-1] + 1
            rawKey = filter[startOfKey:endOfKey]
        if rawKey[0] == " ":
            startOfKey = startOfKey + 1
            rawKey = filter[startOfKey:endOfKey]
        if rawKey[0] == "(":
            startOfKey = startOfKey + 1
            rawKey = filter[startOfKey:endOfKey]

        key = filter[startOfKey:endOfKey]
        return index, key, startOfKey, endOfKey

    def addRecordNameToKeys(self, filter):
        keys = []
        for operation in self.operations:
            lastIndex = 0
            foundAll = False
            while not foundAll:
                index = filter[lastIndex:].find(operation)
                if index != -1:
                    index, key, startOfKey, endOfKey = self.getIndexOfKeys(filter, index, lastIndex)
                    keys.append(
                        {
                            "key": key,
                            "startOfKey": startOfKey,
                            "endOfKey": endOfKey,
                        }
                    )
                    lastIndex = index+len(operation)
                else:
                    foundAll = True
        keys = sorted(keys, key=lambda d: d['startOfKey'])
        filterString = ""
        prevIndex = 0
        for key in keys:
            filterString += filter[prevIndex:key['startOfKey']] + f"record['{key['key']}']"
            prevIndex = key['endOfKey']
        filterString += filter[prevIndex:]
        return filterString

    def filter(self, data, filter):
        filters = self.addRecordNameToKeys(filter)
        filterResults = []
        for record in data:
            if eval(filters):
                filterResults.append(record)
        return filterResults