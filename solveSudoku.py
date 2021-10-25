#Student name: Santiago Romero

import copy 

class evalue:
    def __init__(self):
        self.steps = 0
        self.solved = 0
sc = evalue()
"""
A sudoku is a 9x9 matrix where each item has domain {1,2,3,4,5,6,7,8,9}. 
A sudoku problem contains a incomplete grid where some squares are missing. The missing squares are denoted by 0.
                                8 0 0 0 2 0 0 0 0 
                                0 1 0 6 5 0 8 0 3 
                                0 0 5 0 0 0 2 0 0 
                                0 0 0 2 0 0 6 0 4 
                                0 0 3 0 0 0 0 0 0 
                                2 0 7 0 0 0 5 3 0 
                                5 0 1 4 0 0 0 0 0 
                                0 0 0 0 6 2 0 1 0 
                                0 0 0 0 1 0 4 0 0 

The target is to assign a value to each missing square, such that the following rules will not be violated:
    1. any row contains all values from {1,2,3,4,5,6,7,8,9}
    2. any column contains all values from {1,2,3,4,5,6,7,8,9}
    3. The grid can be divided into 9 3x3 blocks. Each block contains all values from {1,2,3,4,5,6,7,8,9}
    an example of sudoku: 
                                8 6 4 7 2 3 1 9 5 
                                9 1 2 6 5 4 8 7 3 
                                3 7 5 8 9 1 2 4 6 
                                1 5 9 2 3 7 6 8 4 
                                6 8 3 9 4 5 7 2 1 
                                2 4 7 1 8 6 5 3 9 
                                5 2 1 4 7 9 3 6 8 
                                4 3 8 5 6 2 9 1 7 
                                7 9 6 3 1 8 4 5 2 

"""


class point:
    """
        A "point" is a square in the sudoku grid. 
        x,y denotes the horizontal-vertical position of the square.
        "available" is a list of all candidate values for this position.
        "value" is the current value for the position. The dafault is 0.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = []
        self.value = 0


def rowNum(p, sudoku):
    """
    Return  current values in p's row.
    """
    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    row.remove(0)
    return row  # set type


def colNum(p, sudoku):
    """
    Return current values in p's column
    """
    col = []
    length = len(sudoku)
    for i in range(p.x, length, 9):
        col.append(sudoku[i])
    col = set(col)
    col.remove(0)
    return col  # set type


def blockNum(p, sudoku):
    """
    Return current values in p's block
    """
    block_x = p.x // 3
    block_y = p.y // 3
    block = []
    start = block_y * 3 * 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])
    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])
    for i in range(start + 9 + 9, start + 9 + 9 + 3):
        block.append(sudoku[i])
    block = set(block)
    block.remove(0)
    return block  # set type


def initPoint(sudoku):
    """
    Initialise the sudoku grid using the input, and return the candidate positions 
    """
    pointList = []
    length = len(sudoku)
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    p.available.append(j)
            pointList.append(p)
    return pointList
    

def ForwardCheck(pointList, sudoku):
    """
    Task 1: 
    Implement the forward checking algorithm that performs arc consistency checks
    :param pointList: a list which stores all currently unassigned variables. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
    :return: an updated pointList that is the result of the arc consistency algorithm for sudoku
    """
    updatedList = []
    for p in pointList:
        p.available.clear()
        for j in range (1,10):
            if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                p.available.append(j)
        updatedList.append(p)
        
    return updatedList

def BacktrackCSP_frameWork(pointList, sudoku, select=None):
    """
    Task 2: Complete this method in the indicated code segments. 
    
    :param pointList: a list which stores all variables currently unassigned. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
     Note: 0 denotes that this position has not been assigned.
    :return: True (if at least a solution can be find) or False(if no solution exists)
    """
    ##############################
    #Implement the main framework of the backtracking algorithm:
    #Select a value from the available list of the variable "pselected" 
    #Call the ForwardCheck method to perform arc consistency check
    #Check whether assigning value to pselected will result in a conflict
    #Proceed with search or backtrack
    
    
    if len(pointList) <= 0:
        #if testSudoku(sudoku):
            #showSudoku(sudoku)
        return True
    #sc.steps +=1
    #Select the next unassigned variable
    if select == "default": #default function, just use it to support your understanding.
        pselected = select_unassigned_var(pointList, sudoku)
    elif select == "MRV":
        pselected = select_unassigned_var_MRV(pointList, sudoku)
    elif select == "New":
        pselected = select_unassigned_var_New(pointList, sudoku)
    else:
        print("select method undefined!")
        return
    flag = False
    
    for i in range(len(pselected.available)):
        sudoku[pselected.y*9+pselected.x] = pselected.available[i]
        #print((pselected.x,pselected.y),pselected.available[i])
        updatedList = ForwardCheck(pointList, sudoku)
        valid = True
        for p in updatedList:
            if p.available == []:
                valid = False
                
        if valid != False:
            sc.steps += 1
            if BacktrackCSP_frameWork(updatedList, sudoku, select):
                return True
    
        sudoku[pselected.y*9+pselected.x] = 0
        
                
    """sudoku[pselected.y*9+pselected.x] = pselected.available.pop()
    sc.steps+=1
    updatedList = ForwardCheck(pointList, sudoku)
    valid = True
    for p in updatedList:
        if p.available == []:
            valid = False
            break
    if valid == True:
        flag = BacktrackCSP_frameWork(updatedList, sudoku, select)"""  
    #############################
    return flag
    


def testSudoku(sudoku):
    """
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square.
    :return: True (if sudoku is a valid solution), False (otherwise)
    
    Note: If the input is not a valid solution, print out the row, column, or block where a conflict occurs
    """
    for i in range(9):
        nums=set()
        for j in range(9):
            if sudoku[i*9+j]==0:
                print("(%d,%d) is 0"%(i,j))
                return False
            nums.add(sudoku[i*9+j])
        if len(nums)<9:
            print("row: %d"%i)
            return False
    for i in range(9):
        nums=set()
        for j in range(9):
            if sudoku[i + j*9] == 0:
                print("(%d,%d) is 0" % (j, i))
                return False
            nums.add(sudoku[i+j*9])
        if len(nums)<9:
            print("col:%d"%i)
            return False
    for i in range(0,9,3):
        for j in range(0,9,3):
            nums=set()
            nums.update({sudoku[i*9+j], sudoku[i*9+j+1], sudoku[i*9+j+2],
                         sudoku[(i+1)*9+j],sudoku[(i+1)*9+j+1],sudoku[(i+1)*9+j+2],
                         sudoku[(i+2)*9+j],sudoku[(i+2)*9+j+1],sudoku[(i+2)*9+j+2]
                         })
            nums.difference_update({0})
            if len(nums)<9:
                print("(%d,%d)block:"%(i,j))
                return False
    return True

def select_unassigned_var(pointList, sudoku):
    """
    Given a partial assignment for the sudoku puzzle, choose the next unassigned variable, 
    return it and update the "pointList".
    Note: this is the default function for selecting the next unassigned variable.
    """

    return pointList.pop()


def select_unassigned_var_MRV(pointList, sudoku):
    """
    Task 3: 
    Given partial assignment sudoku, choose the next unassigned variable, 
    return it and update "pointList".
    For this task, you need to implement the MRV heuristic for selecting the next unassigned variable.
    :param pointList: a list which stores all variables currently unassigned. Each item here is a "point" entry.
    :param sudoku: current assignments. Each element denotes an assignment to the corresponding square."""
###############################################################################################  #Selecting the next unassigned square by searching through the pointlist and finding the point# #which has the fewest candidate values, if there is a tie, it is broken by selecting the point# #that has the larger amount of assigned neightbours (in that points block)                    # 
###############################################################################################

    MRV_point = 0
    selected_length = len(pointList[0].available)
    selected_block_size = len(blockNum(pointList[0],sudoku))
    for i in range (1,len(pointList)):
        if len(pointList[i].available) == selected_length:
            if len(blockNum(pointList[i],sudoku)) > selected_block_size:
                MRV_point = i
                selected_block_size = len(blockNum(pointList[i],sudoku))
        if len(pointList[i].available) < selected_length:
            MRV_point=i
            selected_block_size = len(blockNum(pointList[i],sudoku))
            selected_length = len(pointList[i].available)
    return pointList.pop(MRV_point)


def select_unassigned_var_New(pointList, sudoku):
    """
    Task 4:
    Given a partial assignment, choose the next unassigned variable, 
    return it and update "pointList".
    For this task you need to implement a different heuristic for selecting the next unassigned variable.     
    """
###############################################################################################
#Selecting the next unassigned point and order its domain using least constraining value (LCV)#
###############################################################################################
    
    #firstly, select the most-constrained-variable(or variable with MRVs).#
    MCV_point = 0
    selected_length = len(pointList[0].available)
    for i in range (1,len(pointList)):
        if len(pointList[i].available) < selected_length:
                MCV_point= i
                selected_length = len(pointList[i].available)
    chosen_point = pointList.pop(MCV_point)

    # calculare the number of rule-outs made by each candidate value and store them in a dictionary #
    sudoku_local = copy.deepcopy(sudoku)
    ruleOut_currMin = 999
    LCV = 0
    my_dict = {}
    for i in range(len(chosen_point.available)):
        sudoku_local[chosen_point.y*9+chosen_point.x] = chosen_point.available[i]
        ruledOut = checkRuleOut(sudoku_local,pointList)
        my_dict[chosen_point.available[i]]= ruledOut
        
    # sort the values by least constraining -> most constraining and add them back to the point's  domain #
    my_dict = dict(sorted(my_dict.items(),key=lambda item:item[1]))
    chosen_point.available = list(my_dict.keys())
    
    return chosen_point
        

def checkRuleOut(sudoku, pointList):
    """
    Return the amount of ruled-out values
    :param sudoku:  The modified sudoku where exact a 0-position's value is filled.
    :param pointList: pointList before modification
    :return: Return the amount of ruled-out values
    """
    length = len(sudoku)
    count = 0
    for i in range(length):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    count += 1
    oldCount = 0
    for k in pointList:
        oldCount += len(k.available)

    return oldCount - count



def check(p, sudoku):
    """Check if position p's trial value violate rules, return True if not violated"""
    if p.value == 0:
        print('not assign value to point p!!')
        return False
    if p.value not in rowNum(p, sudoku) and p.value not in colNum(p, sudoku) and p.value not in blockNum(p, sudoku):
        return True
    else:
        return False


def showSudoku(sudoku):
    """Print the sudoku"""
    for j in range(9):
        for i in range(9):
            print('%d ' % (sudoku[j * 9 + i]), end='')
        print('')
    print("\n")

