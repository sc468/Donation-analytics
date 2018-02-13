
# coding: utf-8
# Goal: Store donation amounts in a custom AVL order statistic Tree,
# allowing O(log(n)) runtimes

#Details:
#AVL Tree: A balanced binary tree that has O(log(n)) complexity for append
#operations.
#Statistic Order Tree: A tree where each node stores the number of elements in
#it's branches. This allows O(log(n)) complexity for rank search and percentile
#retrieval.
#Duplicate values are not added as nodes. Instead, the corresponding node's
#variable "count" is incremented. This requires some changes to the algorithims
#for finding percentile, adding values, rotating the tree, etc

#Unit testing is shown in AVL_Order_Statistic_Tree.ipynb. I observe ~5x to >10x
#speed increases by using AVL trees as opposed to arrays (O(n)) with large data.

#References and Citations
# AVL Tree
# Problem Solving with Algorithms and Data Structures using Python
# Brad Miller and David Ranum, Luther College
# http://interactivepython.org/runestone/static/pythonds/Trees/AVLTreeImplementation.html
#
# Order Statistic Tree
# James Aspnes
# http://www.cs.yale.edu/homes/aspnes/pinewiki/OrderStatisticsTree.html

import math

#Tree node
class Node:


    def __init__(self, val, parent = None):
        self.leftChild = None
        self.rightChild = None
        self.parent = parent
        self.value = val
        self.leftCount = 0
        self.rightCount = 0
        self.count = 1
        self.balance = 0


    def isLeftChild(self):
        return (not self.parent is None) and self.parent.leftChild is self


    def isRightChild(self):
        return (not self.parent is None) and self.parent.rightChild is self


#AVL order statistic tree
class Tree:


    def __init__(self):
        self.root = None
        self.numEntries = 0


    def add(self, val):
        self.numEntries += 1
        if self.root == None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    #Add value to Tree
    #Use standard binary tree algorithm, then check balance and rotate if needed
    def _add(self, val, node):
        if val < node.value:
            node.leftCount += 1
            if node.leftChild is None:
                node.leftChild = Node(val, node)
                self.updateBalance(node.leftChild)
            else:
                self._add(val, node.leftChild)
        elif val > node.value:
            node.rightCount += 1
            if node.rightChild is None:
                node.rightChild = Node(val, node)
                self.updateBalance(node.rightChild)
            else:
                self._add(val, node.rightChild)
        elif val == node.value:
            node.count +=1


    #Update balance of node and parents if needed
    #Balance = left subtree height - right subtree height
    def updateBalance (self, node):
        if node.balance >1 or node.balance <-1:
            self.rebalance(node)
            return
        if not node.parent is None:
            if node.isLeftChild():
                node.parent.balance += 1
            elif node.isRightChild():
                node.parent.balance -=1
            if node.parent.balance !=0:
                self.updateBalance(node.parent)


    def rotateLeft (self, oldRoot):
        newRoot = oldRoot.rightChild
        oldRoot.rightChild = newRoot.leftChild
        if not newRoot.leftChild is None:
            newRoot.leftChild.parent = oldRoot
        newRoot.parent = oldRoot.parent
        if oldRoot is self.root:
            self.root = newRoot
        else:
            if oldRoot.isLeftChild():
                oldRoot.parent.leftChild = newRoot
            else:
                oldRoot.parent.rightChild = newRoot
        newRoot.leftChild = oldRoot
        oldRoot.parent = newRoot
        #Update balance factor of nodes
        oldRoot.balance = oldRoot.balance + 1 - min (newRoot.balance, 0)
        newRoot.balance = newRoot.balance + 1 + max (oldRoot.balance, 0)
        #Update leftCount and rightCount of nodes
        oldRoot.rightCount = newRoot.leftCount
        newRoot.leftCount = oldRoot.rightCount + oldRoot.leftCount + oldRoot.count


    def rotateRight (self, oldRoot):
        newRoot = oldRoot.leftChild
        oldRoot.leftChild = newRoot.rightChild
        if not newRoot.rightChild is None:
            newRoot.rightChild.parent = oldRoot
        newRoot.parent = oldRoot.parent
        if oldRoot is self.root:
            self.root = newRoot
        else:
            if oldRoot.isRightChild():
                oldRoot.parent.rightChild = newRoot
            else:
                oldRoot.parent.leftChild = newRoot
        newRoot.rightChild = oldRoot
        oldRoot.parent = newRoot
        #Update balance factors of nodes
        oldRoot.balance = oldRoot.balance - 1 - max (newRoot.balance, 0)
        newRoot.balance = newRoot.balance - 1 + min (oldRoot.balance, 0)
        #Update leftCount and rightCount of nodes
        oldRoot.leftCount = newRoot.rightCount
        newRoot.rightCount = oldRoot.leftCount + oldRoot.rightCount +oldRoot.count


    def rebalance (self, node):
        if node.balance < 0:
            if node.rightChild.balance > 0:
                self.rotateRight (node.rightChild)
                self.rotateLeft (node)
            else:
                self.rotateLeft(node)
        elif node.balance > 0:
            if node.leftChild.balance < 0:
                self.rotateLeft (node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)


    def printTree (self):
        if not self.root is None:
            self._printTree(self.root)


    def _printTree (self, node):
        if not node is None:
            self._printTree(node.leftChild)
            print ('Value =', node.value, '. Left Count =', node.leftCount, '. Right Count = ', node.rightCount, '. Count = ', node.count)
            self._printTree (node.rightChild)


    def findRank(self, rank):
        if not self.root is None:
            return self._findRank(rank, self.root)
        else:
            return None


    def _findRank(self, rank, node):
        if node.leftChild is None:
            leftCount = 0
        else:
            leftCount = node.leftCount

        if rank >leftCount and rank <= leftCount + node.count:
            return node.value
        elif rank <= leftCount:
            if node.leftChild is None:
                return None
            return self._findRank(rank, node.leftChild)
        elif rank > leftCount + node.count:
            if node.rightChild is None:
                return None
            return self._findRank (rank-leftCount-node.count, node.rightChild)
        else:
            return None


    def findPercentile (self, percentile):
        #Find nearest-rank, given percentile

        #Special case: 0th percentile is rank 1.
        if percentile == 0:
            return self.findRank(1)

        rank = math.ceil(percentile/100*self.numEntries)
        return self.findRank(rank)
