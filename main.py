import DecisionTree
import Node
import FPTreeBuilder
import FPTreeMiner

def main():
	#Insert input file
	"""
	IMPORTANT: Change this file path to change training data
	"""
	data, attributes = DecisionTree.readCVS('AdultCensus_cleaned.csv')
	trainingdata, testdata = DecisionTree.splitData(data, 25000, 5000)
	tree = DecisionTree.makeTree(trainingdata, attributes, 'income', 0)
	print "generated decision tree"
	DecisionTree.decisionTest(testdata,tree, attributes)

def associationAnalysis():
	transactions = [[]]
	with open('AdultCensus_cleaned.csv') as file:
		# skipped the header
	    next(file)
	    for line in file:
	    	line = line.strip("\r\n")
	    	transactions.append(line.split(',')[1:])
	# since we got approximate 30,000 transaction, min support num can't be two small
	min_sup = 150
	headerTable = {}
	counts = []
	
	targetItem1 = '<=50K'
	targetItem2 = '>50K'
	
	fpTreeBuilder = FPTreeBuilder.FPTreeBuilder(transactions, min_sup, counts, headerTable)
	FPTreeMiner.FPTreeMiner(targetItem1, targetItem2, fpTreeBuilder.tree, min_sup, headerTable)



if __name__ == '__main__':
	main()
	associationAnalysis()