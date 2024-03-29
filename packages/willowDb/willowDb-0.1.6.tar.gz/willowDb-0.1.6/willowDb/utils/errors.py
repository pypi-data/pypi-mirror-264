class WillowDbException(Exception):

    class NoTableFound(Exception):
        pass

    class TableAlreadyExists(Exception):
        pass

    class PrimaryKeyNotFound(Exception):
        pass

    class NoIndexFile(Exception):
        pass

    class FileDoesNotExist(Exception):
        pass

    class PrimaryKeyAlreadyUsed(Exception):
        pass