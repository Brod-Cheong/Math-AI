from operator import index
from application.SolveEquation.BinaryTreeClass import BinaryTree
from application.SolveEquation.StackClass import Stack
import re



class Expression():
    def __init__(self,expression):
        self.__expression=expression
        self.__ParseTree= None
        self.__NumberOfBrackets=0
        self.__Length= None
        self.__operators = [['**'], ['*', '/'], ['+','-']]
        self.__Value=0
        super().__init__()
    
    def getLength(self):
        return self.__Length

    def getExpression(self):
        return self.__expression
    def getValue(self):
        return self.__Value
    def getNumberOfBrackets(self):
        return self.__NumberOfBrackets
    
    def checkIfNum(self,token):
        try:
            token=int(token)        #check if is an integer
            return True,token,False
        except:                     
            if('.'in token):        #Check if it is possibly a float
                try:
                    token=float(token)
                    return True,token,False
                except:                     #If it goes to here it means that there are more than one '.' hence instantly an error
                    return False,token,True
            else:
                return False,token,False    #It means that this is most likely either an operator or bracket or even a letter
        

    def Validate_UserInput(self):  # Validate the User Input Expressions
       
        self.__expression = self.__expression.replace(" ","")  #First is to remove any white spaces 
        input=self.__expression

#   To tokenise the input expression, I will be using regex.findall
#       The order of what pattern I want to obtain first is as follow:
#       [()] to extract all opening and closing brackets ----> [*]{2} to extract it first to not confuse it with * for multiplication
#       -----> (?<=[^0-9.)])[-]?[0-9\.]+ which uses positive lookbehind where I will only match possibly negative numbers if to the left of it is an operator or opening bracket
#       -----> (?<![0-9\.\)])[-]?[0-9\.]+ which uses negative lookbehind where I will only match possibly negative numbers if to the left of it is not a nuumber or closing bracket 
#       -----> [^0-9.] to match all operators by selecting non-numbers
#       This allows us to correctly tokenise into open and closing brackets, negative and positive numbers float or integer as well as operators symbol
#                               
        fullySeperatedTokens=re.findall(r"[()]|[*]{2}|(?<=[^0-9.)])[-]?[0-9\.]+|(?<![0-9\.\)])[-]?[0-9\.]+|[^0-9.]", input)

        # Check whether there are equal nuber of open and close bracket
        Count_Open_Bracket=0
        Count_Close_Bracket=0
        listOfNumber=[]         #Store the Numbers
        ListOfOperator=[]       #Store the Operators

        for i in fullySeperatedTokens:
            IsNumber,i, Invalid=self.checkIfNum(i)
            if(Invalid):                
                return False,False,None #Return immediatly since there is an invalid input
            if(IsNumber):
                listOfNumber.append(i)  
            elif i =='(':
                Count_Open_Bracket+=1   
            elif i ==')':
                Count_Close_Bracket+=1
            elif(i=='**'):
                ListOfOperator.append(i)

            elif i in '+-*/':
                ListOfOperator.append(i)
            else:
                return False,False,None  #It is most likey to be a letter or an invalid symbol hence immediately return

        CountOfNumbers=len(listOfNumber)            
        CountOfOperators=len(ListOfOperator)

        if Count_Close_Bracket==Count_Open_Bracket:     #Check if there are equal number of opening and closing brackets
            ValidBracket=True
            self.__NumberOfBrackets=Count_Close_Bracket
        else:
            ValidBracket=False

        if(CountOfNumbers==1):                         #Check If there is only one number for example (1)
            ValidOperators=True
            return ValidOperators,ValidBracket,fullySeperatedTokens

        
        if(CountOfNumbers-1)==CountOfOperators:         #Check if the count of number minus 1 is equal to the count of operators
                                                        # for example (4+5+3), there are 3 numbers and 2 operators
            ValidOperators=True
        else:
            ValidOperators=False
        
        return ValidBracket,ValidOperators,fullySeperatedTokens     #return the necessary variables and the fully seperated tokens
        
    def BuildParseTree(self):
        
        ValidBracket,ValidOperators,fullySeperatedTokens=self.Validate_UserInput()
        if(ValidBracket and ValidOperators):
            
            self.__Length = len(fullySeperatedTokens)
            
            Highest_Precedence='**'

            Second_Highest_Precedence='*/'

            Lowest_Precedence="+-"

            operator_stack = Stack()
            character_stack =Stack()
            
            
            for token in fullySeperatedTokens:
              
                IsNumber,token,__=self.checkIfNum(token)
                if IsNumber:
                    character_stack.push(BinaryTree(key=token))

                elif (token in Second_Highest_Precedence or token in Lowest_Precedence) and (operator_stack.size())>0 and operator_stack.get() in Highest_Precedence:
                    right = character_stack.pop()
                    op = operator_stack.pop()
                    left = character_stack.pop()
                    character_stack.push(BinaryTree(key=op, leftTree=left, rightTree=right))
                    operator_stack.push(token)

                elif token in Lowest_Precedence and operator_stack.size()>0 and operator_stack.get() in Second_Highest_Precedence:
                    right = character_stack.pop()
                    op = operator_stack.pop()
                    left = character_stack.pop()
                    character_stack.push(BinaryTree(key=op,leftTree=left, rightTree=right))
                    operator_stack.push(token)

                elif token == ')':
                    while (operator_stack.size()) > 0 and operator_stack.get() != '(':
                        right = character_stack.pop()
                        op = operator_stack.pop()
                        left = character_stack.pop()
                        character_stack.push(BinaryTree(key=op, leftTree=left, rightTree=right))
                    operator_stack.pop()
                else:
                    operator_stack.push(token)

            while operator_stack.size() > 0:
                right = character_stack.pop()
                op = operator_stack.pop()
                left = character_stack.pop()
                character_stack.push(BinaryTree(key=op, leftTree=left, rightTree=right))

            self.__ParseTree=character_stack.pop()
            error = False
            return error
        else:
            error = True
            self.__ParseTree=None
            return error

    def EvaluateExpression(self):
        self.__Value=self.__ParseTree.EvaluateTree(self.__ParseTree)
        return self.__Value
    