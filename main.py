import DecisionTree
import Node

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
		data.append(line.split(','))
	data.remove([])
	attributes = data[0]
	data.remove(attributes)
	#Run ID3
	tree = DecisionTree.makeTree(data, attributes, target, 0)
	print "generated decision tree"

	testdata = [[]]
	f = open('AdultTest.csv')
	for line in f:
		line = line.strip("\r\n")
		testdata.append(line.split(','))
	testdata.remove([])
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




if __name__ == '__main__':
	main()