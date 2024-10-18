from Classes import *
from Consolidator import *
from Defines import *




if __name__ == "__main__":
    fc = FConsolildator()

    file1 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/amexb_06_24.xlsx"
    file2 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/amexg_06_24.xlsx"
    file3 = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/06/discover_06_24.xlsx"

    fc.addFile(file1)
    fc.addFile(file2)
    fc.addFile(file3)

    fc.analyzeFileList()

    fc.createConsolidatedExcelSheet(".")

    dataFrame = fc.getResultDataFrame()
    dfCreditTransactions = dataFrame.loc[dataFrame["Amount"] > 0.0]

    dfProfiler = DataFrameProfiler(dfCreditTransactions)

    dfProfiler.processDataFrame()

    dfProfiler.createProfileReport()