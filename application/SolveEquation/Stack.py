# Yap Kai Rei (P2021432)
# Alastair theng (P2021490)
# DAAA/2B/05

#---------------------------------
# Class
#---------------------------------

class Stack:
    def __init__(self):
        self.__list= []

    #---------------------------------
    # Getters/Setters
    #---------------------------------
    def getList(self):
        return self.__list 

    #---------------------------------
    # Functions
    #---------------------------------

    def isEmpty(self):
        return self.getList() == []

    def size(self):
        return len(self.getList())

    def clear(self):
        self.getList().clear()

    def push(self, item):
        self.getList().append(item)

    def pop(self):
        if self.isEmpty():
            return None
        else:
            return self.getList().pop()

    def get(self):
        if self.isEmpty():
            return None
        else:
            return self.getList()[-1]

    def toStr(self):
        output = ''
        for i in range( len(self.getList()) ):
            item = self.getList()[i]
            if i < len(self.getList())-1 :
                output += f'{str(item)}'
            else:
                output += f'{str(item)}'
        return output

    def __str__(self):
        output = '<'
        for i in range( len(self.getList()) ):
            item = self.getList()[i]
            if i < len(self.getList())-1 :
                output += f'{str(item)}, '
            else:
                output += f'{str(item)}'
        output += '>'
        return output
