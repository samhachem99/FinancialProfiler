import argparse
import pandas as pd
import enum
import os
from dateutil import parser
from datetime import datetime
from Defines import *

class FConsolidatorBankType(enum.Enum):
    BANK_TYPE_AMEX = "amex"
    BANK_TYPE_APPL = "apple"
    BANK_TYPE_CHSE = "chase"
    BANK_TYPE_BRCL = "barclays"
    BANK_TYPE_DISC = "discover"

    def __str__(self):
        return str(self.value)

class FConsolidatorAmexFileCol(enum.Enum):
    AMEX_FILE_COL_DATE = "Date"
    AMEX_FILE_COL_DESC = "Description"
    AMEX_FILE_COL_AMOUNT = "Amount"
    AMEX_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

class FConsolidatorDiscoverFileCol(enum.Enum):
    DISCOVER_FILE_COL_DATE = "Post date"
    DISCOVER_FILE_COL_DESC = "Description"
    DISCOVER_FILE_COL_AMOUNT = "Amount"
    DISCOVER_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

class FConsolidatorChaseFileCol(enum.Enum):
    CHASE_FILE_COL_DATE = "Transaction Date"
    CHASE_FILE_COL_DESC = "Description"
    CHASE_FILE_COL_AMOUNT = "Amount"
    CHASE_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

class FConsolidatorFileTypes(enum.Enum):
    XLSX = "xlsx"
    CSV = "csv"

    def __str__(self):
        return str(self.value)

class FConsolildator():
    def __init__(self, fileList:list=None):
        self.fileList = fileList if fileList else []
        self.resultDataFrame = None
        self.transactionList = []

    def getResultDataFrame(self):
        self.resultDataFrame = pd.DataFrame(self.transactionList, columns=['Date', 'Description', 'Amount', 'Category'])
        return self.resultDataFrame

    def getFileList(self):
        return self.fileList

    def getTransactionList(self):
        return self.transactionList

    def createConsolidatedExcelSheet(self, directoryPath:str=None):
        filePath = "{}/consolidatedSheet.xlsx".format(directoryPath)

        self.getResultDataFrame()

        self.resultDataFrame.sort_values(by=['Date'], inplace=True)

        with pd.ExcelWriter(filePath) as writer:
            self.resultDataFrame.to_excel(writer)

    def addFile(self, fileNameWithPath: str):
        if fileNameWithPath not in self.fileList:
            self.fileList.append(fileNameWithPath)

    def analyzeFileList(self):
        for file in self.fileList:
            if self.analyzeFile(file) != 0:
                return -1
        return 0

    def analyzeFile(self, fileNameWithPath: str):
        dataFrame = None

        if str(FConsolidatorFileTypes.XLSX) in fileNameWithPath:
            dataFrame = pd.read_excel(fileNameWithPath)
        elif str(FConsolidatorFileTypes.CSV) in fileNameWithPath:
            dataFrame = pd.read_csv(fileNameWithPath)
        else:
            return -2

        if str(FConsolidatorBankType.BANK_TYPE_AMEX) in fileNameWithPath:
            self.analyzeAmexDataFrame(dataFrame)
        elif str(FConsolidatorBankType.BANK_TYPE_CHSE) in fileNameWithPath:
            self.analyzeChaseDataFrame(dataFrame)
        elif str(FConsolidatorBankType.BANK_TYPE_DISC) in fileNameWithPath:
            self.analyzeDiscoverDataFrame(dataFrame)
        elif str(FConsolidatorBankType.BANK_TYPE_BRCL) in fileNameWithPath:
            self.analyzeBarclaysDataFrame(dataFrame)
        elif str(FConsolidatorBankType.BANK_TYPE_APPL) in fileNameWithPath:
            self.analyzeAppleDataFrame(dataFrame)
        else:
            return -1

        return 0

    def analyzeAmexDataFrame(self, dataFrame:pd.DataFrame):
        for idx, transaction in dataFrame.iterrows():
            date = parser.parse(str(transaction[FConsolidatorAmexFileCol.AMEX_FILE_COL_DATE.value]))
            self.transactionList.append([date.strftime(DATE_FORMAT),
                                         " ".join(transaction[FConsolidatorAmexFileCol.AMEX_FILE_COL_DESC.value].split()),
                                         round(transaction[FConsolidatorAmexFileCol.AMEX_FILE_COL_AMOUNT.value], 2),
                                         transaction[FConsolidatorAmexFileCol.AMEX_FILE_COL_CAT.value]])

    def analyzeChaseDataFrame(self, dataFrame:pd.DataFrame):
        for idx, transaction in dataFrame.iterrows():
            date = parser.parse(str(transaction[FConsolidatorChaseFileCol.CHASE_FILE_COL_DATE.value]))
            self.transactionList.append([date.strftime(DATE_FORMAT),
                                        " ".join(transaction[FConsolidatorChaseFileCol.CHASE_FILE_COL_DESC.value].split()),
                                        round(-1.0*transaction[FConsolidatorChaseFileCol.CHASE_FILE_COL_AMOUNT.value], 2),
                                        transaction[FConsolidatorChaseFileCol.CHASE_FILE_COL_CAT.value]])

    def analyzeDiscoverDataFrame(self, dataFrame:pd.DataFrame):
        for idx, transaction in dataFrame.iterrows():
            date = parser.parse(str(transaction[FConsolidatorDiscoverFileCol.DISCOVER_FILE_COL_DATE.value]))
            self.transactionList.append([date.strftime(DATE_FORMAT),
                                        " ".join(transaction[FConsolidatorDiscoverFileCol.DISCOVER_FILE_COL_DESC.value].split()),
                                        round(transaction[FConsolidatorDiscoverFileCol.DISCOVER_FILE_COL_AMOUNT.value], 2),
                                        transaction[FConsolidatorDiscoverFileCol.DISCOVER_FILE_COL_CAT.value]])

    def analyzeBarclaysDataFrame(self, dataFrame:pd.Series):
        pass

    def analyzeAppleDataFrame(self, dataFrame:pd.Series):
        pass


if __name__ == "__main__":
    fc = FConsolildator()

    file1 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/amexb_06_24.xlsx"
    file2 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/amexg_06_24.xlsx"
    file3 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/discover_06_24.xlsx"

    fc.addFile(file1)
    fc.addFile(file2)
    fc.addFile(file3)

    fc.analyzeFileList()

    print(fc.getTransactionList())

    fc.createConsolidatedExcelSheet(".")




