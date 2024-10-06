import json
import argparse
import pandas as pd
import math
from datetime import datetime
from matplotlib import *
import re
from Defines import *
from MCCA.Defines import SearchNodeDateConstraint, SearchNodeName, SearchNodeResultScore, SearchNodeType

class Transaction():
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
    def __init__(self, name: SearchNodeName, expectedScore: SearchNodeResultScore):
        super().__init__(name, SearchNodeType.SEARCH_NODE_TYPE_PRIMARY, SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH, expectedScore)

class FinancialProfiler():
    def __init__(self):
        self.mainNodes = []
