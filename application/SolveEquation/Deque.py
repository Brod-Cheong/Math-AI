# Yap Kai Rei (P2021432)
# Alastair theng (P2021490)
# DAAA/2B/05

#---------------------------------
# Class
#---------------------------------

class Deque: 

    def __init__(self):
        self.__list = [] #empty array

    #---------------------------------
    # Getters/Setters
    #---------------------------------

    def getList(self):
        return self.__list

    #---------------------------------
    # Functions
    #---------------------------------

    # get size of my queue right now
    def size(self):
        return len(self.__list)

    def isEmpty(self):
        return self.__list == []

    #clears all item in list
    def clear(self):
        self.__list.clear()

    #append to list from right
    def addTail(self, item):
        self.__list.append(item)

    #append to list from left
    def addHead(self, item):
        self.__list.insert(0, item)
    
    #removes from list head
    def removeHead(self):
        if self.isEmpty():
            return None
        else:
            return self.__list.pop(0)

    #removes from list tail
    def removeTail(self):
        if self.isEmpty():
            return None
        else:
            return self.__list.pop(-1)

    #retrieves first item in list
    def getHead(self):
        if self.isEmpty():
            return None
        else:
            return self.__list[0]

    #retrieves last item in list
    def getTail(self):
        if self.isEmpty():
            return None
        else:
            return self.__list[-1]

    def __str__(self):
        output = "<"
        for i in range(len(self.__list)):
            item = self.__list[i]
            if i < len(self.__list) - 1:
                output += f'{str(item)},'
            else:
                output += f'{str(item)}'
        output += '>'
        return output