# Example of Naive Bayes implemented from Scratch in Python
import csv
import random
import pandas
import math
import pandas as pd
from pandas import DataFrame, Series

def training(url, target, num, testNum):
    data = pd.read_csv(url, nrows = num)

    testData = pd.read_csv(url, skiprows = num, nrows=num + 1 + testNum)
    testFrame = DataFrame(testData)
    frame = DataFrame(data)
    testFrame.columns = frame.columns
    table = probabilityTable(frame, target)
    return table, frame.income.unique(), testFrame



def func(s):
    temp = s.value_counts()
    return temp / temp.sum()
def probabilityTable(df, target):
    probTable = dict()
    for i in df.columns.values:
        if i != target:
            res = df.groupby(target)[i].apply(func)
            probTable[i] = res
    return probTable

def predictions(table, testData, decisions):
    rightcount = 0.0
    totalcount = len(testData)
    for index, row in testData.iterrows():
        decisionTable = dict()
        for d in decisions:
            value = 1.0
            for c in testData.columns.values[1:-1]:
                try:
                    value += math.log(table[c][d][row[c]],10)

                except KeyError:
                    break
            decisionTable[d] = value
        if argMax(decisionTable) == row[testData.columns.values[-1]]:
            rightcount += 1.0


        print index, decisionTable
    print rightcount/totalcount


def argMax(dct):
    """
    Returns the key with the highest value.
    """
    if len(dct.keys()) == 0: return None
    all = dct.items()
    values = [x[1] for x in all]
    maxIndex = values.index(max(values))
    return all[maxIndex][0]



table , decisions, testData = training('AdultCensus_cleaned.csv', 'income', 25000, 5000)

predictions(table, testData, decisions)


