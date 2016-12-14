import math
from collections import Counter

def argMax(dct):
    if len(dct.keys()) == 0: return None
    all = dct.items()
    values = [x[1] for x in all]
    maxIndex = values.index(max(values))
    return all[maxIndex][0]

def countData(attributes,data,goalAttr):
    index = attributes.index(goalAttr)
    targetVaulues = [line[index] for line in data]
    return Counter(targetVaulues)

def entropy(attributes, data, goalAttr):
    c = countData(attributes,data,goalAttr)
    dataEntropy = sum([(-freq/len(data)) * math.log(float(freq)/len(data), 2) for freq in c.values()])
    return dataEntropy

def gain(attributes, data, attr, targetAttr):
    c = countData(attributes, data, attr)
    subsetEntropy = 0.0
    index = attributes.index(attr)
    for val in c.keys():
        dataSubset = [entry for entry in data if entry[index] == val]
        subsetEntropy += (c[val] / sum(c.values())) * entropy(attributes + [targetAttr], dataSubset, targetAttr)
    return entropy(attributes + [targetAttr], data, targetAttr) - subsetEntropy

def getNextAttr(data, attributes, goalAttr):
    d = dict()
    for a in attributes:
        d[a] = gain(attributes, data, a, goalAttr)
    return argMax(d)

def getValues(data, attributes, attr):
    index = attributes.index(attr)
    values = []
    for line in data:
        if line[index] not in values:
            values.append(line[index])
    return values

def getSubtreeContent(data, attributes, best, val):
    content = list()
    index = attributes.index(best)
    for line in data:
        if line[index] == val:
            line = line[0:index] + line[index+1:]
            content.append(line)
    return content

def init(data, targetAttr, attributes):
    vals = [record[attributes.index(targetAttr)] for record in data]
    c = countData(attributes, data, targetAttr)
    default = max(c, key=lambda k: c[k])
    if len(attributes) <= 1 or not data:
        return default
    if vals.count(vals[0]) == len(vals):
        return vals[0]

    next = getNextAttr(data, attributes[:-1], targetAttr)
    initialtree = dict()
    initialtree[next] = dict()
    for val in getValues(data, attributes, next):
        content = getSubtreeContent(data, attributes, next, val)
        newAttr = attributes[:]
        newAttr.remove(next)
        initialtree[next][val] = init(content, targetAttr, newAttr)
    return initialtree

def predictions(testdata, tree, attributes):
    rightCount = 0.0
    for line in testdata:
        result = tree.copy()
        while type(result) == type(dict()):
            index = attributes.index(result.keys()[0])
            result = result[result.keys()[0]]
            value = line[index]
            if value in result.keys():
                result = result[value]
            else:
                result = "None"
                break
        if result == line[-1]:
            rightCount += 1
    print rightCount / len(testdata)

def readCVS(url):
    file = open(url)
    data = [line.strip("\r\n").split(',')[1:] for line in file]
    attributes = data[0]
    return data[1:], attributes


def splitData(data, trainNum,testNum):
    return data[0:trainNum],data[trainNum + 1: trainNum + testNum]

