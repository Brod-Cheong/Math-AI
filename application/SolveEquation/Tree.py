# Yap Kai Rei (P2021432)
# Alastair theng (P2021490)
# DAAA/2B/05

#---------------------------------
# Imports
#---------------------------------

import matplotlib.pyplot as plt
from application.SolveEquation.Deque import Deque
import math

#---------------------------------
# Functions
#---------------------------------

# Recursive function to determine the locations of nodes in a Binary Tree
def binaryTreePosVertical(G, root, width=1, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):

    # Create position dictionary if doesnt exist
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    # If there is only one node, return
    try:
        children = list(G.neighbors(root))
    except Exception as e:
        return pos

    # children includes the parent in the list
    # so remove it from the list
    if parent is not None:
        children.remove(parent)


    if len(children) != 0:
        # Divide the width by number of child nodes to prevent the width of the tree
        # from increasing as the depth increases and prevents overlapping of nodes
        newWidth = width/len(children)

        # |<--- width --->|
        #
        #       |root|
        #       / | \
        #      /  |  \
        #     /   |   \
        # |  n1   |   n2  |
        #       midpt.

        # n1 and n2 are located in the midpoints of each half



        # Get the new x position of the left node by subtracting the
        # center of the root/parent node by the the new width divided by two
        nextx = xcenter - width/2

        for child in children:
            # Add Location
            # Update the y location (vertical height) by subtracting the current y location by the gap

            pos = binaryTreePosVertical(G, child, width=newWidth, vert_gap=vert_gap,
                                vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)

            # If there is a right node, add back the width to get the new x location of the right node
            nextx += width

    return pos


# Recursive function to determine the locations of nodes in a Binary Tree
def binaryTreePosHorizontal(G, root, width_gap=0.2, width=0, height=1, ycenter=0.5, pos=None, parent=None):

        #         ^
        #         |          ---
        #         |        - n2      <-------- n2 in midpt of the half
        #         |       /  ---
        #         |      /
        #  height |  root -- midpt
        #         |      \
        #         |       \  ---
        #         |        - n1      <-------- n1 in midpt of the half
        #         v          ---


    # Create position dictionary if doesnt exist
    if pos is None:
        pos = {root: (width, ycenter)}
    else:
        pos[root] = (width, ycenter)

    # If there is only one node, return
    try:
        children = list(G.neighbors(root))
    except Exception as e:
        return pos, False


    if parent is not None:
        children.remove(parent)


    if len(children) != 0:
        # Divide the height by number of child nodes to prevent the height of the tree
        # from increasing as the depth increases and prevents overlapping of nodes
        newY = height/len(children)


        # Get the new y position of the left node by subtracting the
        # center of the root/parent node by the the new height divided by two
        nexty = ycenter - height/2

        for child in children:
            # Add Location
            # Update the x location (vertical height) by subtracting the current x location by the gap
            pos= binaryTreePosHorizontal(G, child, width_gap=0.2, width=width+width_gap, height=newY, ycenter=nexty, pos=pos, parent=root)

            # If there is a right node, add back the height to get the new y location of the right node
            nexty += height

    return pos

#---------------------------------
# Class
#---------------------------------

class BinaryTree:
    # Access functions
    def __init__(self, key, symbol, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree
        self.symbol = symbol

    #---------------------------------
    # Functions
    #---------------------------------
    def getDepth(self, tree):
        if tree is None:
            return -1 
    
        else :
            # Compute the depth of each subtree
            leftDepth = self.getDepth(tree.leftTree)
            rightDepth = self.getDepth(tree.rightTree)
    
            # Get deeper depth
            if (leftDepth > rightDepth):
                return leftDepth+1
            else:
                return rightDepth+1

    def printInorder(self, level):
        if self.rightTree != None:
            self.rightTree.printInorder(level+1)

        print(str(level*self.symbol) + str(self.key))

        if self.leftTree != None:
            self.leftTree.printInorder(level+1)



    def printVertical(self):

        # Setup rough dimensions of the binary tree 
        depth = self.getDepth(self)

        if depth > 5:
            inp = input("Tree produced is deeper than 5 levels and may become distorted.\nContinue with console print?\nEnter 'y' to continue printing, or any other key to quit \n")
            if inp == "y":
                pass
            else:
                return


        # 2^n , n is the depth
        numNodesInLastLayer = 2**depth

        # Let number of cells to for last row such that:
        # node<space>node<space>node<space>...
        numCells = numNodesInLastLayer + numNodesInLastLayer-1


        # Extract Nodes for each depth layer using Breadth-First Search
        deque = Deque()
        deque.addHead(self)

        # Dictionary to store nodes at each depth
        # {depth:[n1, n2, ...]}
        depthDict = {0:[self.key]}
        
        currentDepth = 1
        nodesEncountered = 0

        while currentDepth <= depth:
            #  From the head:
            #   Add left child of the head to tail
            #   Add right child of the head to tail
            #   Remove Head (parent)
            #
            #  Continue until no nodes are left

            currentTree = deque.getHead()

            depthItems = []
            

            # Try-Except used to capture nodes which are not trees, eg. whitespaces " "
            # Add values of trees if available
            # else, add whitespaces
            try:
                if currentTree.leftTree != None:
                    # Add to tail
                    deque.addTail(currentTree.leftTree)
                    depthItems.append(currentTree.leftTree.key)

                else:
                    depthItems.append(" ")
                    deque.addTail(" ")
            except:
                depthItems.append(" ")
                deque.addTail(" ")

            
            try:
                if currentTree.rightTree != None:
                    # Add to tail
                    deque.addTail(currentTree.rightTree)
                    depthItems.append(currentTree.rightTree.key)

                else:
                    depthItems.append(" ")
                    deque.addTail(" ")
            except:
                depthItems.append(" ")
                deque.addTail(" ")


            # Used to keep track how many nodes have been iterated through
            # for calculating if the next depth has been reached
            nodesEncountered += 2


            # Add items to current depth
            try:
                depthDict[currentDepth] = depthDict[currentDepth] + depthItems
            except:
                depthDict[currentDepth] = depthItems
            
            if nodesEncountered == 2**currentDepth:
                # Add depth
                currentDepth += 1

                # reset number to 0 for new depth
                nodesEncountered = 0

            # Remove the head
            deque.removeHead()



        matrix = []

        width = numCells

        # To add nodes that do not overlap,
        # Keep dividing the space that nodes occupy by 2
        for i in range(0, depth+1):
            row = []
            timesToSplit = 2**i
            midIndex = math.floor(width / 2)

            # For final row
            if i == depth:
                for j in range(numCells):
                    # Add the value every 2 cells
                    if j % 2 == 0:
                        row.append(str(depthDict[i].pop(0)))
                    else:
                        # Add space to try and match the previous item's length
                        space = len(matrix[-1][j])
                        row.append(space * " ")

                matrix.append(row)

            else:
                # For other rows
                for j in range(timesToSplit):

                    # Eg. at depth 1, split the row into 2 parts
                    # Depth 0: [" ",   " ", " ", Node0, " ",  " ",  " "]

                    # Depth 1: [" ", Node1, " "] [" "] [" ", Node2, " "]
                    #                  ^                        ^
                    #                  |                        |
                    # Minirows ---------------------------------

                    miniRow = []
                    for cell in range(int((numCells-(timesToSplit-1))/timesToSplit)):

                        #
                        if cell == midIndex:
                            try:
                                miniRow.append(str(depthDict[i].pop(0)))
                            except:
                                miniRow.append(" ")
                        else:
                            miniRow.append(" ")

                    if j == range(timesToSplit)[-1]:
                        row = row + miniRow
                    else:
                        row = row + miniRow + [" "]

                
                # Add branches if the row is not the first
                if (i != 0):
                    branchRow = []
                    encounteredOpen = False
                    # Open Branch = /
                    # Closed branch = \

                    for cell in row:
                        if cell != " ":
                            if not encounteredOpen:
                                lengthOfItem = len(row[row.index(cell)])
                                # Add spaces to match the position of the item
                                branchRow.append((lengthOfItem-1)*" " + "/")
                                encounteredOpen = True
                            else:
                                branchRow.append("\\")
                                encounteredOpen = False

                        else:
                            if encounteredOpen:
                                # Add top-space character between open and closed branches
                                branchRow.append(chr(8254))
                            else:
                                # Else, add space
                                branchRow.append(" ")

                    matrix.append(branchRow)

                matrix.append(row)


                # Apply branch for final row
                if (i + 1) == depth:
                    branchRow = []

                    # 1 for /, 2 for \
                    branch = 1
                    itemCounter = 0
                    for h in range(numCells):
                        if h % 2 == 0:
                            if depthDict[i+1][itemCounter] == ' ':
                                branchRow.append(" ")

                            else:
                                if branch == 1:
                                    branchRow.append("/")
                                    branch += 1
                                else:
                                    branchRow.append("\\")
                                    branch -= 1

                            itemCounter += 1

                        else:
                            lengthOfRoot = len(matrix[-1][h])
                            branchRow.append(lengthOfRoot * " ")

                    matrix.append(branchRow)

            # Get new width of each node
            width = math.floor(width / 2)

        for row in matrix:
            # Print all the rows
            print(" ".join(row))



    def plotTree(self, orientation):
        # Extract nodes and edges using Breadth First Search Traversal
        # Since networkx requires values to be unique when connecting edges, a unique ID has to be assigned to each node to prevent duplicate nodes
        nodeDict = {}
        edgeList = []

        deque = Deque()

        # Start with root
        # Add id and current tree
        deque.addHead({0: self})

        # Extract the values of the root
        [(rootID, root)] = deque.getHead().items()

        # Assign the ID to the value of the node
        nodeDict[rootID] = root.key

        # Extract the longest value
        maxLen = len(str(root.key))

        while deque.size() > 0:
            #  From the head:
            #   Add left child of the head to tail
            #   Add right child of the head to tail
            #   Remove Head (parent)
            #
            #  Continue until no nodes are left

            currentParent = deque.getHead()
            [(currentID, currentTree)] = currentParent.items()

            if currentTree.leftTree != None:
                # Get NextID
                [(nextID, _)] = deque.getTail().items()
                nextID += 1

                # Add to tail
                deque.addTail({nextID: currentTree.leftTree})

                # Add the edges (ParentID, ChildID)
                edgeList.append((currentID, nextID))

                # Add node to dictionary
                nodeDict[nextID] = currentTree.leftTree.key

                # Check if the length is larger than current
                if len(str(currentTree.leftTree.key)) > maxLen:
                    maxLen = len(str(currentTree.leftTree.key))

            if currentTree.rightTree != None:
                # Get NextID
                [(nextID, _)] = deque.getTail().items()
                nextID += 1

                # Add to tail
                deque.addTail({nextID: currentTree.rightTree})

                # Add the edges (ParentID, ChildID)
                edgeList.append((currentID, nextID))

                # Add node to dictionary
                nodeDict[nextID] = currentTree.rightTree.key

                # Check if the length is larger than current
                if len(str(currentTree.rightTree.key)) > maxLen:
                    maxLen = len(str(currentTree.rightTree.key))

            # Remove the head
            deque.removeHead()

        # Create graph
        G = nx.Graph()

        # Scale node size based on largest number length
        if maxLen > 2:
            nodeSize = 300 + ((maxLen-2) * 200)
        else:
            nodeSize = 300

        # If only one node exists, just show the single node
        if len(nodeDict) == 1:
            G.add_node(nodeDict[0])
            nx.draw(G, with_labels=True, node_color=[
                    "blue"], node_size=nodeSize, font_color='white', font_size=10)
            plt.show()
            return

        G.add_edges_from(edgeList)

        # Networkx does not support tree printing natively
        # Use a function to determine the location of the nodes manually
        # Pos is a dictionary containing the location of nodes: {node:(x, y), ...}
        if orientation == 1:
            pos = binaryTreePosHorizontal(G, 0)
        else:
            pos = binaryTreePosVertical(G, 0)

        # Add nodes based on the locations
        nx.draw(G, pos=pos, with_labels=False, node_color=["blue"] + ["lightcyan"]*(len(nodeDict)-1), node_size=nodeSize)

        # Add mask to the nodes based on the nodeDict
        nx.draw_networkx_labels(G, pos, nodeDict, font_size=10, font_color='black')

        plt.show()

        return
