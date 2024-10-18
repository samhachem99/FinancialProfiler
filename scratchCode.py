import re
from Defines import *
import pandas as pd
import json
from datetime import datetime
from Classes import *

if __name__ == "__main__":
    month = 8

    regexList = ["DFW AIRPORT", "DFW", "AIRPORT", "DFWAIRPORT"]

    # stringInQuestion0 = "DFW AIRPORT"
    categoryInQuestion1 = "Merchandise & Supplies-Groceries"
    descriptionInQuestion1 = "AplPay 7-ELEVEN 3978DFW AIRPORT TX"

    categoryInQuestion2 = "Other-Government Services"
    descriptionInQuestion2 = "DFW AIRPORT PARKING DFW AIRPORT TX"

    categoryInQuestion3 = "Shopping"
    descriptionInQuestion3 = "COSTCO WHSE #0664"

    categoryInQuestion4 = "Restaurant-Bar & Café"
    descriptionInQuestion4 = "AplPay IN-N-OUT DALLDALLAS TX"

    df = pd.read_excel("{}0{}/summary_0{}.xlsx".format(BASE_FOLDER_ADDRESS, month, month))
    dfCreditTransactions = df.loc[df["Amount"] > 0.0]

    dfProfile1Obj = DataFrameProfiler(dfCreditTransactions)

    dfProfile1Obj.saveProfileToFile()

    dfProfile1Obj.createProfileReport()
