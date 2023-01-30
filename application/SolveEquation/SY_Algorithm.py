# Yap Kai Rei (P2021432)
# Alastair theng (P2021490)
# DAAA/2B/05

# ---------------------------------
# Imports
#---------------------------------

from application.SolveEquation.Stack import Stack
from application.SolveEquation.Tree import BinaryTree

#---------------------------------
# Class
#---------------------------------

class SY:
    # Shunting-Yard Algorithm to standardize inputs to build parse tree
    # Algorithm adapted from: http://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/


    def __init__(self):
        self.__symbols = ["+", "-", "*", "/", "**", "(", ")"]
        
        #                    Ordered by level of precedence
        #    
        #                    Least                                                                             Most  
        #                    Impt                                                                              Impt  
        #                    -------------------------------------------------------------------------------------> 
        self.__operatorsDict = {"+":[0, "left"], "-":[0, "left"], "*":[1, "left"], "/":[1, "left"], "**":[2, "right"]}


    #---------------------------------
    # Getters / Setters
    #---------------------------------

    def getSymbols(self):
        return self.__symbols

    def getOperatorsDict(self):
        return self.__operatorsDict


    #---------------------------------
    # Functions
    #---------------------------------

    # Add try-except blocks
    def buildTree(self, tokens, treeSymbol="."):
        operatorStack = Stack()
        operandStack = Stack()


        for char in tokens:
            # handle value
            
            if char not in self.getSymbols():
                if "." in char:
                    char = float(char)
                else:
                    char = int(char)

                # handle the value into a tree
                operandStack.push(BinaryTree(char, treeSymbol))

            # handle operators
            if char in self.getSymbols():
                if operatorStack.isEmpty():
                    operatorStack.push(f"{char}")

                elif char == "(":
                    operatorStack.push(f"{char}")

                elif char == ")":
                    # handle the operands into trees until a "(" is met in the operator stack 
                    while not operatorStack.isEmpty():
                        if operatorStack.get() != "(":
                            popOperator = operatorStack.pop()

                            right = operandStack.pop()
                            left = operandStack.pop()

                            operandStack.push(BinaryTree(popOperator, symbol=treeSymbol, leftTree=left, rightTree=right))
                        else:
                            # Discard the left bracket
                            operatorStack.pop()
                            break
                    
                else:
                    while not operatorStack.isEmpty():
                        if operatorStack.get() in ["(", ")"]:
                            break

                        # Step 6 in the Guide
                        # Pop operators with (higher precedence than incoming) OR (same precedence as incoming and is left-associative)
                        # And handle the operands into trees, then add the incoming operator
                        if (self.getOperatorsDict()[operatorStack.get()][0] > self.getOperatorsDict()[char][0]) or (self.getOperatorsDict()[char][1]=="left" and (self.getOperatorsDict()[operatorStack.get()][0] == self.getOperatorsDict()[char][0])):
                            popOperator = operatorStack.pop()
                            right = operandStack.pop()
                            left = operandStack.pop()

                            operandStack.push(BinaryTree(popOperator, symbol=treeSymbol, leftTree=left, rightTree=right))

                        # Step 5 in the Guide
                        # Else if incoming operator is of (higher precedence than top of stack) OR (is of same precedence and right-associative)
                        elif (self.getOperatorsDict()[operatorStack.get()][0] < self.getOperatorsDict()[char][0]) or (self.getOperatorsDict()[char][1]=="right" and (self.getOperatorsDict()[operatorStack.get()][0] == self.getOperatorsDict()[char][0])):
                            break

                    operatorStack.push(f"{char}")

        # handle remaining operators in stack 
        while not operatorStack.isEmpty():
            popOperator = operatorStack.pop()
            right = operandStack.pop()
            left = operandStack.pop()
            operandStack.push(BinaryTree(popOperator, symbol=treeSymbol, leftTree=left, rightTree=right))
            

        # Return tree
        return operandStack.pop()

                
                