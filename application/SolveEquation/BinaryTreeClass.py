class BinaryTree:
    def __init__(self,key = None, leftTree = None, rightTree = None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getLeftTree(self):
        return self.leftTree

    def getRightTree(self):
        return self.rightTree 
    
    def insertLeft(self, key = None):
        if self.leftTree == None:
            self.leftTree = BinaryTree(key)
        else:
            t = BinaryTree(key)
            self.leftTree , t.leftTree = t, self.leftTree

    def insertRight(self, key = None):
        if self.rightTree == None:
            self.rightTree = BinaryTree(key)
        else:
            t =BinaryTree(key)
            self.rightTree , t.rightTree = t, self.rightTree


    def EvaluateTree(self,Tree):
        
        leftTree= Tree.getLeftTree()
        rightTree= Tree.getRightTree()
        operator = Tree.getKey()
        
        if leftTree!= None and rightTree!= None:   
            
            if operator == '+':
                return self.EvaluateTree(leftTree) + self.EvaluateTree(rightTree)
            elif operator == '-':
                return self.EvaluateTree(leftTree) - self.EvaluateTree(rightTree)
            elif operator == '*':
                return self.EvaluateTree(leftTree) * self.EvaluateTree(rightTree)
            elif operator == '/':
                return self.EvaluateTree(leftTree) / self.EvaluateTree(rightTree)
            elif operator == '**':
                return self.EvaluateTree(leftTree) ** self.EvaluateTree(rightTree)  
                    
        else:
            return Tree.getKey()
