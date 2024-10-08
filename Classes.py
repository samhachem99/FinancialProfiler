import json
import argparse
import pandas as pd
import math
from datetime import datetime
from matplotlib import *
import re
from Defines import *

class Transaction():
    def __init__(self, dfTransaction: pd.Series):
        self.date = dfTransaction["Date"]
        self.description = dfTransaction["Description"]
        self.category = dfTransaction["Category"]
        self.amount = dfTransaction["Amount"]

        self.primaryNode = None
        self.secondaryNode = None

    def __init__(self, date, description, category, amount):
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def getDescription(self):
        return self.description

    def getCategory(self):
        return self.category

    def getAmount(self):
        return self.amount

    def __str__(self):
        string = {
            "transactionDate": self.date,
            "transactionDescription": self.description,
            "transactionCategory": self.category,
            "transactionAmount": self.amount,
        }

        return string

class Node():
    def __init__(self, name: SearchNodeName, type: SearchNodeType, timeConstraint: SearchNodeDateConstraint, expectedScore: SearchNodeResultScore):
        # Initialization based on parameter input.
        self.name = name
        self.type = type
        self.timeConstraint = timeConstraint
        self.expectedScore = expectedScore

        self.categoryKeywords = []
        self.categoryExceptions = []

        self.descriptionKeywords = []
        self.descriptionExceptions = []

        self.totalAmount = 0.0
        self.transactionCount = 0
        self.transactions = [Transaction]

    def getCategoryKeywords(self):
        return self.categoryKeywords

    def getCategoryExceptions(self):
        return self.categoryExceptions

    def getDescriptionKeywords(self):
        return self.descriptionKeywords

    def getDescriptionExceptions(self):
        return self.descriptionExceptions

    def addCategoryKeyword(self, keyword: str):
        self.categoryKeywords.append(keyword)

    def setCategoryKeywords(self, keywords: list):
        self.categoryKeywords = keywords

    def addDescriptionKeyword(self, keyword: str):
        self.descriptionKeywords.append(keyword)

    def setDescriptionKeyword(self, keywords: list):
        self.descriptionKeywords = keywords

    def addCategoryException(self, exception: str):
        self.categoryExceptions.append(exception)

    def setCategoryException(self, exceptions: list):
        self.categoryExceptions = exceptions

    def addDescriptionException(self, exception: str):
        self.descriptionExceptions.append(exception)

    def setDescriptionException(self, exceptions: list):
        self.descriptionExceptions = exceptions

    def addTransaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.totalAmount += transaction.getAmount()
        self.transactionCount += 1

    def __str__(self):
        string = {
            "node_name": self.name,
            "node_type": self.type,
            "total_amount": self.totalAmount,
            "transaction_count": self.transactionCount,
            "transactions": self.transactions
        }

        return string

class PrimaryNode(Node):
    def __init__(self, name: SearchNodeName, expectedScore: SearchNodeResultScore, secondaryNodes: list = []):
        super().__init__(name, SearchNodeType.SEARCH_NODE_TYPE_PRIMARY, SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH, expectedScore)
        self.secondaryNodes = secondaryNodes

    def getSecondaryNodes(self):
        self.secondaryNodes

    def setSecondaryNodes(self, secondaryNodes: pd.Series):
        self.secondaryNodes = secondaryNodes

    def addSecondaryNode(self, secondaryNode: pd.Series):
        self.secondaryNodes.append(secondaryNode)

class SecondaryNode(Node):
    def __init__(self, name: SearchNodeName, timeConstraint: SearchNodeDateConstraint, expectedScore: SearchNodeResultScore):
        super().__init__(name, SearchNodeType.SEARCH_NODE_TYPE_SECONDARY, timeConstraint, expectedScore)

class TransactionAnalyzer:
    def __init__(self, transaction: pd.Series):
        self.transaction = transaction
        self.transactionProfile = {}

    def setTransaction(self, transaction: pd.Series):
        self.transaction = transaction

    def getTransaction(self):
        return self.transaction

    def getTransactionProfile(self):
        self.buildTransactionProfile()
        return self.transactionProfile

    def extractTens(self, value: int):
        return (value // 10 % 10) * 10

    def isTransactionWeekday(self):
        # Subtracting 1 becuase transactions usually take a full day to clear, especially on weekends.
        return (datetime.strptime(self.transaction["Date"], DATE_FORMAT).weekday() - 1) not in [4, 5, 6] # weekend days: Friday, Saturday, and Sunday.

    def getFilteredString(self, stringInQuestion: str):
        finalString = stringInQuestion

        for string in FILTER_OUT_STRINGS:
            match = re.search(string, stringInQuestion)
            if match:
                finalString = "{}{}".format(stringInQuestion[:match.start()],  stringInQuestion[match.end():])

        return finalString.strip().replace(" ", "")

    def getCompareStringScore(self, stringInQuestion: str, regexString: str):
        score = 0.0
        stringInQuestionTrimmed = self.getFilteredString(stringInQuestion)
        regexStringTrimmed = self.getFilteredString(regexString)

        numMatches = len(re.findall(regexStringTrimmed, stringInQuestionTrimmed))
        match = re.search(regexStringTrimmed, stringInQuestionTrimmed)

        if match != None:
            score = round(((match.end() - match.start()) / len(stringInQuestionTrimmed)) * numMatches, 3)

        return score

    def getMatchScore(self, stringInQuestion: str, regexList: list):
        if len(regexList) == 0:
            return 0
        else:
            return max([self.getCompareStringScore(stringInQuestion, regexString) for regexString in regexList])

    def processTransactionWithNode(self, node):
        overallScore = 0
        expectedScore = node["expected_score"].value

        if  (node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY and \
                not self.isTransactionWeekday()) or \
            (node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY and \
                self.isTransactionWeekday()):
                return overallScore

        categoryKeywordScore = self.getMatchScore(self.transaction["Category"], node["category"]["keywords"])
        categoryExceptionScore = self.getMatchScore(self.transaction["Category"], node["category"]["exceptions"])
        descriptionKeywordScore = self.getMatchScore(self.transaction["Description"], node["Description"]["keywords"])
        descriptionExceptionScore = self.getMatchScore(self.transaction["Description"], node["Description"]["exceptions"])

        if self.extractTens(expectedScore) == SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH.value:
            if categoryExceptionScore == 0 and descriptionExceptionScore == 0:
                overallScore = (categoryKeywordScore) + descriptionKeywordScore
        else:
            if descriptionExceptionScore == 0:
                overallScore =  descriptionKeywordScore

        return overallScore

    def getSecondaryNodeProfile(self, node):
        if len(node["sub"]) == 0:
            return None

        scoreList = pd.Series([self.processTransactionWithNode(node) for node in node["sub"]])

        return None if scoreList.max() == 0 else node["sub"][scoreList.idxmax()]

    def buildTransactionProfile(self):
        scoreList = pd.Series([self.processTransactionWithNode(node) for node in categoryNodes])
        maxScore = scoreList.max()
        maxIdx = scoreList.idxmax()
        nodeHit = None
        secondaryNodeHit = None

        if maxScore == 0:
            maxIdx = -1
            nodeHit = misc_node
        else:
            nodeHit = categoryNodes[maxIdx]
            secondaryNodeHit = self.getSecondaryNodeProfile(categoryNodes[maxIdx])

        transactionProfile = {
            "dfTransactionInfo": {
                "name": self.transaction["Description"],
                "category": self.transaction["Category"],
            },
            "scoreList": scoreList.tolist(),
            "BestNode": nodeHit,
            "BestSecondaryNode": secondaryNodeHit,
        }

        self.transactionProfile = transactionProfile

        return self.transactionProfile

    def __str__(self):
        return str(self.transactionProfile)

class DataFrameProfiler():
    objectCounter = 0

    def __init__(self, dataFrame: pd.DataFrame):
        self.dataFrame = dataFrame
        self.dataFrameProfile = []
        self.isProfileComplete = False
        DataFrameProfiler.objectCounter += 1
        self.fileName = "dataFrameProfile_{}.json".format(DataFrameProfiler.objectCounter)

    def processDataFrame(self):
        self.dataFrameProfile = [TransactionAnalyzer(transaction).getTransactionProfile() for idx, transaction in self.dataFrame.iterrows()]
        self.isProfileComplete = True
        return self.dataFrameProfile

    def getDataFrameProfile(self):
        if not self.isProfileComplete:
            self.processDataFrame()

        return self.dataFrameProfile

    def saveProfileToFile(self):
        if not self.isProfileComplete:
            self.processDataFrame()

        # Save the array to the JSON file
        with open(self.fileName, "w") as f:
            json.dump(self.dataFrameProfile, f)

    def __str__(self):
        return str(self.dataFrameProfile)

class FinancialProfiler():
    def __init__(self):
        self.mainNodes = []
