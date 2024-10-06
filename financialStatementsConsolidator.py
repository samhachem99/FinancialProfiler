import json
import operator
import argparse
import pandas as pd
import enum
import os
from datetime import datetime
from matplotlib import *

class BankType(enum.Enum):
    BANK_TYPE_AMEX = "amex"
    BANK_TYPE_APPL = "apple"
    BANK_TYPE_CHSE = "chase"
    BANK_TYPE_BRCL = "barclays"
    BANK_TYPE_DISC = "discover"

    def __str__(self):
        return str(self.value)

class AmexFileCol(enum.Enum):
    AMEX_FILE_COL_DATE = "Date"
    AMEX_FILE_COL_DESC = "Description"
    AMEX_FILE_COL_AMOUNT = "Amount"
    AMEX_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

class DiscoverFileCol(enum.Enum):
    DISCOVER_FILE_COL_DATE = "Trans. date"
    DISCOVER_FILE_COL_DESC = "Description"
    DISCOVER_FILE_COL_AMOUNT = "Amount"
    DISCOVER_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

class ChaseFileCol(enum.Enum):
    CHASE_FILE_COL_DATE = "Transaction Date"
    CHASE_FILE_COL_DESC = "Description"
    CHASE_FILE_COL_AMOUNT = "Amount"
    CHASE_FILE_COL_CAT = "Category"

    def __str__(self):
        return str(self.value)

BASE_FOLDER_ADDRESS = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/"

FSC_month = 0

FSC_filesInDir = []

FSC_transactionsList = []

class FileTypes(enum.Enum):
    XLSX = "xlsx"
    CSV = "csv"

def FSC_init():
    global parser
    parser = argparse.ArgumentParser(description="Simple XLSX analyzer for financial statments")
    parser.add_argument("-m", "--month", type=str, help="Month (integer) to analyze within the Records folder", required=True)

def FSC_Directory(month):
    pass

def FSC_analyzeFile(month: str, fileName: str):

    if str(BankType.BANK_TYPE_AMEX) in fileName:
        FSC_analyzeAmex(month, fileName)
    elif str(BankType.BANK_TYPE_CHSE) in fileName:
        FSC_analyzeChase(month, fileName)
    elif str(BankType.BANK_TYPE_DISC) in fileName:
        FSC_analyzeDiscover(month, fileName)
    elif str(BankType.BANK_TYPE_BRCL) in fileName:
        FSC_analyzeAmex(month, fileName)
    elif str(BankType.BANK_TYPE_APPL) in fileName:
        FSC_analyzeAmex(month, fileName)

def FSC_analyzeAmex(month: str, fileName: str):
    pathToFile = "{}0{}/{}".format(BASE_FOLDER_ADDRESS, month, fileName)

    print(pathToFile)

    df = pd.read_excel(pathToFile)

    for idx, transaction in df.iterrows():
        FSC_transactionsList.append([transaction[AmexFileCol.AMEX_FILE_COL_DATE.value],
                                    " ".join(transaction[AmexFileCol.AMEX_FILE_COL_DESC.value].split()),
                                    transaction[AmexFileCol.AMEX_FILE_COL_AMOUNT.value],
                                    transaction[AmexFileCol.AMEX_FILE_COL_CAT.value]])

def FSC_analyzeChase(month: str, fileName: str):
    pathToFile = "{}0{}/{}".format(BASE_FOLDER_ADDRESS, month, fileName)

    print(pathToFile)

    df = pd.read_csv(pathToFile)

    for idx, transaction in df.iterrows():
        FSC_transactionsList.append([transaction[ChaseFileCol.CHASE_FILE_COL_DATE.value],
                                     " ".join(transaction[ChaseFileCol.CHASE_FILE_COL_DESC.value].split()),
                                    -1.0*transaction[ChaseFileCol.CHASE_FILE_COL_AMOUNT.value],
                                    transaction[ChaseFileCol.CHASE_FILE_COL_CAT.value]])

def FSC_analyzeDiscover(month: str, fileName: str):
    pathToFile = "{}0{}/{}".format(BASE_FOLDER_ADDRESS, month, fileName)

    print(pathToFile)

    # df = pd.read_excel(pathToFile)

def FSC_scanAndRetrieveFilesFromDirectory(month: str):
    # Construct path to folder
    pathToSearch = "{}0{}/".format(BASE_FOLDER_ADDRESS, month)

    for root, dirs, files in os.walk(pathToSearch):
        for file in files:
            if file.lower().endswith(".{}".format(FileTypes.XLSX.value)) or \
                file.lower().endswith(".{}".format(FileTypes.CSV.value)):
                FSC_filesInDir.append(file)

    if len(FSC_filesInDir) == 0:
        print("ERROR: no files found in directory. .xlsx and .csv are the only two file types accepted")
        return -1
    else:
        return 0

def validateInputs(month: str):
    try:
        if int(month) > 12 or int(month) < 1:
            print("ERROR: Invalid month")
            return -1
    except:
        print("ERROR: Month must be an integer")
        return -1

    return 0

def FSC_createFile(month: str):
    pathToFile = "{}0{}/{}.xlsx".format(BASE_FOLDER_ADDRESS, month, "summary_0{}".format(month))
    pathToImg = "{}0{}/{}.pdf".format(BASE_FOLDER_ADDRESS, month, "summary_0{}".format(month))

    df = pd.DataFrame(FSC_transactionsList, columns=['Date', 'Description', 'Amount', 'Category'])

    df.sort_values(by=['Date'], inplace=True)

    with pd.ExcelWriter(pathToFile) as writer:
        df.to_excel(writer)

def FSC_execute(month: int):
    # validate month
    if validateInputs(month) == -1:
        return

    # validate month
    if validateInputs(month) == -1:
        return

    # Retrieve all files
    if FSC_scanAndRetrieveFilesFromDirectory(month) == -1:
        return

    for i, file in enumerate(FSC_filesInDir):
        FSC_analyzeFile(month, file)

    FSC_createFile(month)

def main():
    FSC_init()

    # Retrieve month from user in string format.
    FSC_month = vars(parser.parse_args())['month']

    # validate month
    if validateInputs(FSC_month) == -1:
        return

    # Retrieve all files
    if FSC_scanAndRetrieveFilesFromDirectory(FSC_month) == -1:
        return

    for i, file in enumerate(FSC_filesInDir):
        FSC_analyzeFile(FSC_month, file)

    FSC_createFile(FSC_month)


if __name__ == "__main__":
    main()