import ceasylog.LoggerLevel as LoggerLevel


class LoggerConfiger(object):
    def __init__(self):
        self.__name = "default"

        self.__maxPrintLevel = LoggerLevel.CRITICAL
        self.__minPrintLevel = LoggerLevel.DEBUG
        self.__maxRecordLevel = LoggerLevel.CRITICAL
        self.__minRecordLevel = LoggerLevel.WARN

        self.__printTimeFormat = "%Y-%m-%d %H:%M:%S.%f"
        self.__recordTimeFormat = "%Y-%m-%d %H:%M:%S.%f"
        self.__recordPathNameFormat = "%Y-%m-%d"

        self.__isRecordB = False
        self.__recordPath = "./"

    @property
    def name(self):
        return self.__name

    @property
    def maxPrintLevel(self):
        return self.__maxPrintLevel

    @property
    def minPrintLevel(self):
        return self.__minPrintLevel

    @property
    def maxRecordLevel(self):
        return self.__maxRecordLevel

    @property
    def minRecordLevel(self):
        return self.__minRecordLevel

    @property
    def printTimeFormat(self):
        return self.__printTimeFormat

    @property
    def recordTimeFormat(self):
        return self.__recordTimeFormat

    @property
    def recordPathNameFormat(self):
        return self.__recordPathNameFormat

    @property
    def isRecordB(self):
        return self.__isRecordB

    @property
    def recordPath(self):
        return self.__recordPath

    def setName(self, name: str):
        self.__name = name

    def setMaxPrintLevel(self, maxPrintLevel):
        self.__maxPrintLevel = maxPrintLevel

    def setMinPrintLevel(self, minPrintLevel):
        self.__minPrintLevel = minPrintLevel

    def setMaxRecordLevel(self, maxRecordLevel):
        self.__maxRecordLevel = maxRecordLevel

    def setMinRecordLevel(self, minRecordLevel):
        self.__minRecordLevel = minRecordLevel

    def setPrintTimeFormat(self, printTimeFormat: str):
        self.__printTimeFormat = printTimeFormat

    def setRecordTimeFormat(self, recordTimeFormat: str):
        self.__recordTimeFormat = recordTimeFormat

    def setRecordPathNameFormat(self, printTimeFormat: str):
        self.__printTimeFormat = printTimeFormat

    def isRecord(self, path: str):
        self.__isRecordB = True
        self.__recordPath = path

    def setRecordPath(self, recordPath: str):
        self.__recordPath = recordPath
