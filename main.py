import DecisionTree
import Node
import FPTreeBuilder
import FPTreeMiner

def main():
	#Insert input file
	"""
	IMPORTANT: Change this file path to change training data
	"""
	file = open('AdultCensus_cleaned.csv')
	"""
	IMPORTANT: Change this variable too change target attribute
	"""
	target = 'income'
	data = [[]]
	for line in file:
		line = line.strip("\r\n")
		data.append(line.split(',')[1:])
	data.remove([])
	attributes = data[0]
	data.remove(attributes)
	trainingdata = data[0:(len(data)* 19 /20)]
	tree = DecisionTree.makeTree(trainingdata, attributes, target, 0)
	print "generated decision tree"

	testdata = data[(len(data)* 19 /20):]
	count = 0
	rightCount = 0.0
	for entry in testdata:
		count += 1
		tempDict = tree.copy()
		result = ""
		while (isinstance(tempDict, dict)):
			root = Node.Node(tempDict.keys()[0], tempDict[tempDict.keys()[0]])
			tempDict = tempDict[tempDict.keys()[0]]
			index = attributes.index(root.value)
			value = entry[index]
			if (value in tempDict.keys()):
				child = Node.Node(value, tempDict[value])
				result = tempDict[value]
				tempDict = tempDict[value]
			else:
				print "can't process input %s" % count
				result = "?"
				break
		if result == entry[-1]:
			rightCount += 1

		print ("entry%s = %s" % (count, result))
	print rightCount / count

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
  	
	fpTreeBuilder = FPTreeBuilder.FPTreeBuilder(formedTransactions, min_sup, counts, headerTable)
	FPTreeMiner.FPTreeMiner(targetItem1, targetItem2, fpTreeBuilder.tree, min_sup, headerTable)



if __name__ == '__main__':
	main()
	associationAnalysis()