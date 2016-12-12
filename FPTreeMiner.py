import FPTreeBuilder
import copy

class FPTreeMiner(object):
    def __init__(self, targetItem1, targetItem2, TreeGrowth, min_sup, headerTable):
        self.min_sup = min_sup
        self.targetItem1 = targetItem1
        self.targetItem2 = targetItem2
        self.treeMining(TreeGrowth=TreeGrowth, headerTable=headerTable)
        
    
    """
    Recursively mining the frequent itemsets in FP-Tree.
    """
    def treeMining(self, TreeGrowth, alpha=[], headerTable={}):
        beta = []
        allNodesOnPath = {}
        currNode = TreeGrowth.root
        childrenNum = len(currNode.children)
        while childrenNum > 0:
            #if not single path, break the loop
            if childrenNum != 1:
                break
            # get next node
            currNode = currNode.children.values()[0]
            allNodesOnPath.setdefault(currNode.data, currNode.count)
            childrenNum = len(currNode.children)
        if len(currNode.children) >= 1:
            for item in headerTable:
                if alpha:
                    for element in alpha:
                        if element != []:
                            tempCopy = copy.copy(element)
                            beta.append(tempCopy)
                            beta.append([item] + tempCopy)
                else:
                    beta.append([item])
                pattern, counts = self.getPatternBaseByItem(headerTable, item)
                nextHeaderTable = {}
                # create a new one
                conditionTree = FPTreeBuilder.FPTreeBuilder(pattern, self.min_sup, counts, nextHeaderTable)
                # if condition tree is not none
                if conditionTree.tree.root.children:
                    tree = conditionTree.tree
                    # recursion
                    self.treeMining(tree, beta, nextHeaderTable)
                beta = []
        else:
            # only one path in the tree
            frequentSet = self.getFrequentSet(allNodesOnPath, alpha)
            #print the result   
            for fItem in frequentSet:
                index = len(fItem) - 1
                items = fItem[0:index] 
                if self.targetItem1 in items or self.targetItem2 in items:
                    if len(items) >= 3:
                        print tuple(items),':',fItem[index]
        return 
    
    # get pattern base of an item by searching header table
    def getPatternBaseByItem(self, headerTable, item):
        pattern = []
        countList = []
        addressList = headerTable[item]
        for address in addressList:
            # store all the items shown in pattern
            itemsInPattern = []
            node = address.parent
            # if current node is root
            if node.data == 'null':
                continue
            # backTrace
            while node.data != 'null':
                itemsInPattern.append(node.data)
                node = node.parent
            itemsInPattern = tuple(itemsInPattern)
            pattern.append(itemsInPattern)
            countList.append(address.count)
        return pattern, countList
            
              
    # find frequent set for tree which only has a single path
    def getFrequentSet(self, items, alpha):
        candidates = self.getCombinations(items.keys())
        result = []
        for element in candidates[::-1]:
            # find element whose count is minimum, result is elementMin
            elementMin = items[element[0]]
            for key in element:
                elementMin = min(elementMin, items[key])
            if self.min_sup <= elementMin:
                for elemInAlpha in alpha:
                    if elemInAlpha:
                        temp = element
                        temp = temp + elemInAlpha
                        temp.append(elementMin)
                        result.append(temp)         
            else:
                candidates.remove(element)

        return result
    
        
    def getCombinations(self, nodes):
        temp = []
        for num in range(1, len(nodes) + 1):
            combinations = []
            positions = [0] * num
            def addOn(listI, nI):
                if num == nI:
                    combinations.append(copy.copy(positions))
                    return
                for listJ in xrange(listI, len(nodes)):
                    positions[nI] = nodes[listJ]
                    addOn(listJ + 1, nI + 1)
            addOn(0,0)
            temp += combinations
        
        return temp  
        