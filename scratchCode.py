import re
from MCCA.Defines import *
import pandas as pd
import json
from datetime import datetime


def compare_strings(string1, string2, how: int):
    return re.search(re.compile(string2.lower()), string1.lower()) != None

def MCCA_extractTens(value: int):
    return (value // 10 % 10) * 10

def isTransactionWeekday(transaction: pd.DataFrame):
    # Subtracting 1 becuase transactions usually take a full day to clear, especially on weekends.
    return (datetime.strptime(transaction["Date"], DATE_FORMAT).weekday() - 1) not in [4, 5, 6] # weekend days: Friday, Saturday, and Sunday.

def getFilteredString(stringInQuestion: str):
    finalString = stringInQuestion

    for string in FILTER_OUT_STRINGS:
        match = re.search(string, stringInQuestion)
        if match:
            finalString = "{}{}".format(stringInQuestion[:match.start()],  stringInQuestion[match.end():])

    return finalString.strip().replace(" ", "")

def getCompareStringScore(stringInQuestion: str, regexString: str):
    score = 0.0
    stringInQuestionTrimmed = getFilteredString(stringInQuestion)
    regexStringTrimmed = getFilteredString(regexString)

    numMatches = len(re.findall(regexStringTrimmed, stringInQuestionTrimmed))
    match = re.search(regexStringTrimmed, stringInQuestionTrimmed)

    if match != None:
        score = round(((match.end() - match.start()) / len(stringInQuestionTrimmed)) * numMatches, 3)

    return score

def getMatchScore(stringInQuestion: str, regexList: list):
    if len(regexList) == 0:
        return 0
    else:
        return max([getCompareStringScore(stringInQuestion, regexString) for regexString in regexList])

def processTransactionWithNode(transaction, node):
    overallScore = 0
    expectedScore = node["expected_score"].value

    if  (node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY and \
            not isTransactionWeekday(transaction)) or \
        (node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY and \
            isTransactionWeekday(transaction)):
            return overallScore

    categoryKeywordScore = getMatchScore(transaction["Category"], node["category"]["keywords"])
    categoryExceptionScore = getMatchScore(transaction["Category"], node["category"]["exceptions"])
    descriptionKeywordScore = getMatchScore(transaction["Description"], node["Description"]["keywords"])
    descriptionExceptionScore = getMatchScore(transaction["Description"], node["Description"]["exceptions"])

    if MCCA_extractTens(expectedScore) == SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH.value:
        if categoryExceptionScore == 0 and descriptionExceptionScore == 0:
            overallScore = (categoryKeywordScore) + descriptionKeywordScore
    else:
        if descriptionExceptionScore == 0:
            overallScore =  descriptionKeywordScore

    return overallScore

def buildTransactionsProfile(df: pd.DataFrame):
    credit_transactions = df.loc[df["Amount"] > 0.0]
    transactionList = []

    for idx, transaction in credit_transactions.iterrows():
        scoreList = [processTransactionWithNode(transaction, node) for node in categoryNodes]

        transaction = {
            "idx": idx,
            "dfTransactionInfo": {
                "name": transaction["Description"],
                "category": transaction["Category"],
            },
            "scoreList": scoreList
        }

        transactionList.append(transaction)

    # Specify the file name
    file_name = "{}0{}/transactionList_0{}.json".format(BASE_FOLDER_ADDRESS, month, month)

    # Save the array to the JSON file
    with open(file_name, "w") as f:
        json.dump(transactionList, f)



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

    df = pd.read_excel("{}0{}/summary_0{}.xlsx".format(BASE_FOLDER_ADDRESS, month, month))

    transaction = df.loc[18]

    print(transaction)

    print(processTransactionWithNode(transaction, food_node))
    print(processTransactionWithNode(transaction, ti_food_node))
    print(processTransactionWithNode(transaction, food_weekday_node))
    print(processTransactionWithNode(transaction, food_weekend_node))