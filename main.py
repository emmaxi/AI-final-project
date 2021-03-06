import DecisionTree
import NaiveBayes
import SVM
from numpy import *

TrainingDataNum = 20000
TestDataNum = 2000
GoalAttr = 'income'


def predicitions():
    """
    Decision Tree:
    """

    print "test different training set"

    for num in range(4000, 20001, 4000):
        print 'dataset number:' + str(num)
        data, attributes = DecisionTree.readCVS('AdultCensus_cleaned.csv')
        print 'decision tree'
        trainingdata, testdata = DecisionTree.splitData(data, num, TestDataNum)
        tree = DecisionTree.init(trainingdata, GoalAttr, attributes)
        DecisionTree.predictions(testdata, tree, attributes)
        print 'naive bayes'
        table, decisions, testData = NaiveBayes.training('AdultCensus_cleaned.csv', GoalAttr, num,
                                                         TestDataNum)
        NaiveBayes.predictions(table, testData, decisions)
    print "test different attributes"
    for i in range(6, 10):
        print str(i) + ":"
        data, attributes = DecisionTree.readCVS('AdultCensus_cleaned-' + str(i) + '.csv')
        trainingdata, testdata = DecisionTree.splitData(data, TrainingDataNum, TestDataNum)
        tree = DecisionTree.init(trainingdata, GoalAttr, attributes)
        print "decision tree:"
        DecisionTree.predictions(testdata, tree, attributes)
        print "naive bayes:"
        table, decisions, testData = NaiveBayes.training('AdultCensus_cleaned-' + str(i) + '.csv', GoalAttr, TrainingDataNum,
                                                         TestDataNum)
        NaiveBayes.predictions(table, testData, decisions)

    print "generate SVM"
    SVM.classify()

import FPTreeBuilder
import FPTreeMiner
import time
from apyori import apriori

def associationAnalysis():
    transactions = [[]]
    formedTransactions = [[]]

    # customized training data
    file = open('AdultCensus_cleaned.csv')
    for line in file:
        line = line.strip("\r\n")
        transactions.append(line.split(',')[1:])
    transactions.remove([])
    headerList = transactions[0]
    for transaction in transactions:
        trans = []
        for i in range(len(transaction)):
            item = transaction[i]
            attributeName = headerList[i]
            trans.append(attributeName + ':' + item)
        formedTransactions.append(trans)
    formedTransactions = formedTransactions[2:]

    # since we got approximate 30,000 transaction, min support num can't be two small
    min_sup = 150
    headerTable = {}
    counts = []

    targetItem1 = 'income:<=50K'
    targetItem2 = 'income:>50K'

    print('Using FP-Growth algorithm to find the frequent pattern in given census:(min_sup is 150 by default)')
    start_timeFP = time.time()
    fpTreeBuilder = FPTreeBuilder.FPTreeBuilder(formedTransactions, min_sup, counts, headerTable)
    FPTreeMiner.FPTreeMiner(targetItem1, targetItem2, fpTreeBuilder.tree, min_sup, headerTable)
    print("---FP-Growth using %s seconds ---" % (time.time() - start_timeFP))
    
    print('Using Apriori library to find the frequent pattern in given census:')
    start_timeA = time.time()
    aprioriResults = list(apriori(formedTransactions))
    print("---Apriori using %s seconds ---" % (time.time() - start_timeA))


if __name__ == '__main__':
    predicitions()
    associationAnalysis()
