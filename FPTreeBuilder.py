class TreeNode(object):
    def __init__(self, data=-1, count=0, parent=None):
        self.data = data
        self.count = count
        self.parent = parent
        self.children = {}
        
class TreeGrowth(object):
    def __init__(self, data=-1, parent=None, itemTable=None):
        self.root = TreeNode(data='null', parent=self)
        # it seems like "frequent item list"
        self.itemTable = itemTable
    
    def addTransaction(self, transaction, Rroot, count):
        if len(transaction) > 0:
            node = Rroot
            currElement = transaction.pop(0)
            if currElement in node.children:
                nextNode = node.children[currElement]
            else:
                """
                create a new node according to the current element in frequent item list.
                Add it into the path.
                """
                newNode = TreeNode(data=currElement, parent=node)
                node.children.setdefault(currElement, newNode)
                nextNode = newNode
            # update the count regardless it's in node.children or not
            nextNode.count += 1
            if nextNode not in self.itemTable[currElement]:
                self.itemTable[currElement].append(nextNode)
            self.addTransaction(transaction, nextNode, count)
        return
                
class FPTreeBuilder(object):
    def __init__(self, transactions, min_sup, counts=[], headerTable={}):
        # transactions: transaction dataset
        self.transactions = transactions
        self.min_sup = min_sup
        # the list of the count of each item
        self.countLists = counts
        
        # Given the whole transactions, get all items and count the frequency of them.
        items = {}
        for transaction in transactions:
            for item in transaction:
                items.setdefault(item, 0)
                items[item] = items[item] + 1
                
        # sorted the items by counts
        sortedQualifiedItems = []
        from operator import itemgetter, methodcaller
        sortedAllItems = sorted(items.iteritems(), key = itemgetter(1), reverse=True)
        for item in sortedAllItems:
            itemName, count = item
            if count >= self.min_sup:
                sortedQualifiedItems.append(itemName)

        self.sortedItems = sortedQualifiedItems
        
        self.itemsTable = self.generateItemsTable(headerTable)
        self.tree = self.buildTree(self.countLists)
          
    
    def buildTree(self, countLists):
        fpTree = TreeGrowth(itemTable=self.itemsTable)
        for transaction in self.transactions:
            # get the sorted transaction in the same order of self.sortedItems
            sortedTransaction = []
            for item in self.sortedItems:
                if item in transaction:
                    sortedTransaction.append(item)
            
            if not countLists:
                count = 1
            else:
                count = countLists.pop(0)
            currentRoot = fpTree.root
            fpTree.addTransaction(sortedTransaction, currentRoot, count)
        return fpTree

    def generateItemsTable(self, itemsTable):
        for item in self.sortedItems:
            itemsTable.setdefault(item, [])
        return itemsTable                    