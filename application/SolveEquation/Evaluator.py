# Yap Kai Rei (P2021432)
# Alastair theng (P2021490)
# DAAA/2B/05

#---------------------------------
# Imports
#---------------------------------

import re 
import os
from application.SolveEquation.Tree import BinaryTree
from application.SolveEquation.Stack import Stack
from application.SolveEquation.SY_Algorithm import SY


#---------------------------------
# Class
#---------------------------------

class Evaluator:
    def __init__(self, currentPath, treeSymbol, functionGroup):
        self.__run = True
        self.__currentPath = currentPath
        self.__treeSymbol = treeSymbol
        self.__functionGroup = functionGroup
        self.__SY = SY()

    
        # Capture Operators----------------------------------------------------|
        #                                                                      | 
        # Capture Exponents---------------------------------------------|      |
        #                                                               |      |
        # Capture integers/floats---------------------------|           |      |
        #                                                   |           |      |
        # Capture negative signs first---------|            |           |      |
        #                                      |            |           |      |
        self.__parseRegex = re.compile("(?<![0-9]|[)]|[.])[-]?[0-9\.]+|[*]{2}|[^0-9\.]")

    #---------------------------------
    # Getters / Setters
    #---------------------------------

    def getSY(self):
        return self.__SY
    
    def getTreeSymbol(self):
        return self.__treeSymbol 

    def getGroup(self):
        return self.__functionGroup

    def getFilePath(self):
        return self.__currentPath 

    def getRegex(self):
        return self.__parseRegex



    #---------------------------------
    # Functions
    #---------------------------------

    def evaluate(self, tree, functionGroup):
        leftTree = tree.leftTree
        rightTree = tree.rightTree
        op = tree.key

        if functionGroup == "1":
            if leftTree != None and rightTree != None:
                if op == '+':
                    return self.evaluate(leftTree, functionGroup) + self.evaluate(rightTree, functionGroup)
                elif op == '-':
                    return self.evaluate(leftTree, functionGroup) - self.evaluate(rightTree, functionGroup)
                elif op == '*':
                    return self.evaluate(leftTree, functionGroup) * self.evaluate(rightTree, functionGroup)
                elif op == '**':
                    return self.evaluate(leftTree, functionGroup) ** self.evaluate(rightTree, functionGroup)
                elif op == '/':
                    return self.evaluate(leftTree, functionGroup) / self.evaluate(rightTree, functionGroup)
            else:
                return tree.key
        else:
            if leftTree != None and rightTree != None:
                if op == '+':
                    return max(self.evaluate(leftTree, functionGroup) , self.evaluate(rightTree, functionGroup))
                elif op == '-':
                    return min(self.evaluate(leftTree, functionGroup) , self.evaluate(rightTree, functionGroup))
                elif op == '*':
                    return round(self.evaluate(leftTree, functionGroup) * self.evaluate(rightTree, functionGroup))
                elif op == '**':
                    return round(self.evaluate(leftTree, functionGroup) % self.evaluate(rightTree, functionGroup))
                elif op == '/':
                    return round(self.evaluate(leftTree, functionGroup) / self.evaluate(rightTree, functionGroup))
            else:
                return tree.key


    def tokenize(self, inputs):
        tokens = self.getRegex().findall(inputs)
        return tokens



    def buildParseTree(self, inputs, printMode=1, orientation=1, enablePrint=False):

        tree = self.getSY().buildTree(inputs, self.getTreeSymbol())

        if enablePrint:
            if printMode == 1:
                if orientation == 1:
                    tree.printInorder(0)
                elif orientation == 2:
                    tree.printVertical()
                else:
                    tree.printInorder(0)

                return tree

            elif printMode == 2:
                if orientation == 1:
                    tree.plotTree(1)
                elif orientation == 2:
                    tree.plotTree(2)
                else:
                    tree.plotTree(2)
                    
                return tree

            else: 
                if orientation == 1:
                    tree.printInorder(0)
                    tree.plotTree(1)
                elif orientation == 2:
                    tree.printVertical()
                    tree.plotTree(2)
                else:
                    tree.printInorder(0)
                    tree.plotTree(2)

                return tree

        else:
            return tree


    def evaluateSingleExpression(self, expression, printMode=1, orientation=1, enablePrint=False):
        tree = self.buildParseTree(expression, printMode=printMode, orientation=orientation, enablePrint=enablePrint)
        return self.evaluate(tree, self.getGroup())
