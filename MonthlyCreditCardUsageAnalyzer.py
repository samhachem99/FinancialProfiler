# Python Dependencies
import json
import argparse
import pandas as pd
import math
from datetime import datetime
from matplotlib import *
import re

# Includes
from Defines import *
from financialStatementsConsolidator import *

def MCCA_init():
    global parser
    parser = argparse.ArgumentParser(description="Simple XLSX analyzer for financial statments")
    parser.add_argument("-m", "--month", type=str, help="Month (integer) to analyze within the Records folder", required=True)

def MCCA_writeNodesToFile(month: int):
    pathToNodesFile = "{}0{}/nodes_0{}.json".format(BASE_FOLDER_ADDRESS, month, month)
    pathToOutputExcelFile = "{}0{}/nodes_summary_0{}.xlsx".format(BASE_FOLDER_ADDRESS, month, month)

    list_For_excel = []

    for node in nodes_list:
        output_dict["nodes"].append({
            "node_name": node["node_name"],
            "node_type": node["node_type"],
            "total_amount": node["total_amount"],
            "transaction_count": node["transaction_count"],
            "transactions": node["transactions"],
        })

    for node in nodes_list:
        list_For_excel.append({
            "Node Name": node["node_name"].value,
            "Node Type": node["node_type"].value,
            "Node Total Amount": node["total_amount"],
            "Node Transaction Count": node["transaction_count"],
        })

    nodesSummary = pd.DataFrame(list_For_excel, columns=["Node Name", "Node Type", "Node Total Amount", "Node Transaction Count"])

    with open(pathToNodesFile, "w") as final:
        json.dump(output_dict, final)

    with pd.ExcelWriter(pathToOutputExcelFile) as writer:
        nodesSummary.to_excel(writer)

def MCCA_extractTens(value: int):
    return (value // 10 % 10) * 10

def MCCA_compareStrings(string1, string2):
    return re.search(re.compile(string2.lower()), string1.lower()) != None


def MCCA_matchInArray2(targetString, node):
    keywords = node["keywords"]
    exceptions = node["exceptions"]

    keyword_score = 0
    exceptions_score = 0

    for string in keywords:
        if targetString == string:
            keyword_score = SearchNodeElementSearchType.SEARCH_NODE_ELEMENT_TYPE_EXACT_MATCH.value
        elif MCCA_compareStrings(targetString, string):
            keyword_score = SearchNodeElementSearchType.SEARCH_NODE_ELEMENT_TYPE_PARTIAL_MATCH.value

def MCCA_matchInArray(string1, array):
    for elem in array:
        if MCCA_compareStrings(string1, elem):
            return True
    else:
        return False

def MCCA_is_transaction_weekday(transaction: pd.DataFrame):
    # Subtracting 1 becuase transactions usually take a full day to clear, especially on weekends.
    return (datetime.strptime(transaction["Date"], DATE_FORMAT).weekday() - 1) not in [4, 5, 6] # weekend days: Friday, Saturday, and Sunday.

def MCCA_does_transaction_match(transaction: pd.DataFrame, node: dict):
    overall_score = 0
    expected_score = node["expected_score"].value

    if MCCA_extractTens(expected_score) == SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH.value:
        if MCCA_matchInArray(transaction["Category"], node["category"]["keywords"]) and \
            not MCCA_matchInArray(transaction["Category"], node["category"]["exceptions"]) and \
            not MCCA_matchInArray(transaction["Description"], node["Description"]["exceptions"]) or \
        (MCCA_matchInArray(transaction["Description"], node["Description"]["keywords"]) and \
            not MCCA_matchInArray(transaction["Description"], node["Description"]["exceptions"])):
                overall_score = 10
    else:
        if MCCA_matchInArray(transaction["Description"], node["Description"]["keywords"]) and \
            not MCCA_matchInArray(transaction["Category"], node["category"]["exceptions"]):
            overall_score = 20

    if overall_score != 0:
        if node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY and \
            MCCA_is_transaction_weekday(transaction):
            overall_score += 1
        elif node["time_constraints"] == SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKEND and \
            not MCCA_is_transaction_weekday(transaction):
            overall_score += 2

    if overall_score == node["expected_score"].value:
        node["total_amount"] += math.ceil(transaction["Amount"])
        node["transaction_count"] += 1

        node["transactions"].append({
            "transaction_date": transaction["Date"],
            "transaction_name": transaction["Description"],
            "transaction_amount": transaction["Amount"],
        })

    return overall_score == node["expected_score"].value

def MCCA_processDataFrame(df: pd.DataFrame):
    credit_transactions = df.loc[df["Amount"] > 0.0]
    overall_hit = 0

    for idx, transaction in credit_transactions.iterrows():
        hit = False
        hit_count = 0

        for node in nodes_list:
            if MCCA_does_transaction_match(transaction, node):
                hit = True
                if node["node_type"] == SearchNodeType.SEARCH_NODE_TYPE_PRIMARY:
                    hit_count += 1

        if hit_count > 1:
            output_dict["multi_hit_transactions"].append({
                "transaction_date": transaction["Date"],
                "transaction_name": transaction["Description"],
                "transaction_amount": transaction["Amount"],
            })

        if hit:
            overall_hit += 1
        else:
            output_dict["no_hit_transactions"].append({
                "transaction_date": transaction["Date"],
                "transaction_name": transaction["Description"],
                "transaction_amount": transaction["Amount"],
            })

    output_dict["total_amount"] = sum(credit_transactions["Amount"])
    output_dict["transaction_count"] = len(credit_transactions["Amount"])
    output_dict["transaction_hits"] = overall_hit

def MCCA_execute(month: int):

    # Consolidate all files.
    FSC_execute(month)

    df = pd.read_excel("{}0{}/summary_0{}.xlsx".format(BASE_FOLDER_ADDRESS, month, month))

    MCCA_processDataFrame(df)

    MCCA_writeNodesToFile(month)

def main():
    MCCA_init()

    # Retrieve month from user in string format.
    MCCA_month = vars(parser.parse_args())['month']

    MCCA_execute(MCCA_month)




if __name__ == "__main__":
    main()