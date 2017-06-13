# -*- coding:utf-8 -*-
import numpy as np

def strategy(state):
    """ Information provided to you:
    state = (board, last_move, playing, board_size)
    board = (x_stones, o_stones)
    stones is a set contains positions of one player's stones. e.g.
        x_stones = {(8,8), (8,9), (8,10), (8,11)}
    playing = 0|1, the current player's index

    Your strategy will return a position code for the next stone, e.g. (8,7)
    """
    def old_evaluation_function(state):
        board, last_move, playing, board_size = state
        row = board_size
        col = board_size
        table = np.zeros([row, col])
        # create a table to record the board state
        # 1: occupied by self
        # -1: occupied by opponent
        # 0: available
        for i in range(row):
            for j in range(col):
                if playing == 1:
                    if (i+1, j+1) in board[0]:
                        table[i, j] = -1
                    elif (i+1, j+1) in board[1]:
                        table[i, j] = 1
                else:
                    if (i+1, j+1) in board[0]:
                        table[i, j] = 1
                    elif (i+1, j+1) in board[1]:
                        table[i, j] = -1

        def score(fiveTuple):
            if len(fiveTuple) != 5:
                print "ERROR"
                return None
            if 1 in fiveTuple and -1 in fiveTuple:
                return 0
            elif sum(fiveTuple) == 0:
                return 7
            elif sum(fiveTuple) == -1:
                return -35
            elif sum(fiveTuple) == -2:
                return -800
            elif sum(fiveTuple) == -3:
                return -15000
            elif sum(fiveTuple) == -4:
                return -800000
            elif sum(fiveTuple) == -5:
                return -10000000
            elif sum(fiveTuple) == 5:
                return 10000000
            elif sum(fiveTuple) == 1:
                return 15
            elif sum(fiveTuple) == 2:
                return 400
            elif sum(fiveTuple) == 3:
                return 1800
            elif sum(fiveTuple) == 4:
                return 100000

        def heuristic(table):
            sumScore = 0
            for i in range(row):
                for j in range(col):
                    if j + 4 < col:
                        sumScore += score(tuple(table[i, j:j + 5]))
                    if i + 4 < row:
                        sumScore += score(tuple(table[i:i + 5, j]))
                    if i + 4 < row and j + 4 < col:
                        fivetuple = []
                        for k in range(5):
                            fivetuple.append(table[i + k, j + k])
                        sumScore += score(tuple(fivetuple))
                    if i + 4 < row and j - 4 >= 0:
                        fivetuple = []
                        for k in range(5):
                            fivetuple.append(table[i + k, j - k])
                        sumScore += score(tuple(fivetuple))
            return sumScore

        scoreTable = {}
        for i in range(row):
            for j in range(col):
                if table[i, j] == 0:
                    table[i, j] = 1
                    scoreTable[(i, j)] = heuristic(table)
                    table[i, j] = 0
        choice = max(scoreTable.items(), key=lambda x: x[1])[0]
        return (choice[0]+1, choice[1]+1)




    def new_evaluation_function(state):
        board, last_move, playing, board_size = state
        row = board_size
        col = board_size
        # create a table to record the board state
        # 1: occupied by self
        # 2: occupied by opponent
        # 0: available
        table = np.zeros([row, col])
        for i in range(row):
            for j in range(col):
                if playing == 1:
                    if (i+1, j+1) in board[0]:
                        table[i, j] = 2
                    elif (i+1, j+1) in board[1]:
                        table[i, j] = 1
                else:
                    if (i+1, j+1) in board[0]:
                        table[i, j] = 1
                    elif (i+1, j+1) in board[1]:
                        table[i, j] = 2
        # 获取该点4个方向的棋型
        def getstring(point):
            x = point[0]
            y = point[1]
            # vertical
            getLine1 = ''
            for k in range(max(x - 4, 0), min(x + 5, 15)):
                getLine1 += str(int(table[k, y]))
            if x-4<0: getLine1 = '*'+getLine1
            if x+4>14: getLine1 = getLine1+'*'
            # horizonal
            getLine2 = ''
            for k in range(max(y - 4, 0), min(y + 5, 15)):
                getLine2 += str(int(table[x, k]))
            if y-4<0: getLine2 = '*'+getLine2
            if y+4>14: getLine2 = getLine2+'*'
            # Oblique 45
            getLine3 = ''
            bx = max(0, x - 4)
            by = max(0, y - 4)
            ux = min(14, x + 4)
            uy = min(14, y + 4)
            for k in range(max(bx - x, by - y), min(ux - x, uy - y)+1):
                getLine3 += str(int(table[x + k, y + k]))
            if x-4<0 or y-4<0: getLine3 = '*'+getLine3
            if x+4>14 or y+4>14: getLine3 = getLine3+'*'
            # Oblique 135
            getLine4 = ''
            for k in range(max(bx - x, y - uy), min(ux - x, y - by)+1):
                getLine4 += str(int(table[x + k, y - k]))
            if x-4<0 or y+4>14: getLine4 = '*'+getLine4
            if x+4>14 or y-4<0: getLine4 = getLine4+'*'

            return [getLine1, getLine2, getLine3, getLine4]

        # 判断我方棋型
        def judgeType1(getline):
            if '11111' in getline:
                return 'win5'
            if '011110' in getline:
                return 'alive4'
            if '211110' in getline or '011112' in getline\
                    or '*11110' in getline or '01111*' in getline:
                return 'die4'
            if '11101' in getline or '10111' in getline\
                or '11011' in getline:
                return 'lowdie4'
            if '001110' in getline or '011100' in getline:
                return 'alive3'
            if '211100' in getline or '001112' in getline\
                or '*11100' in getline or '00111*' in getline\
                or '211010' in getline or '010112' in getline\
                or '*11010' in getline or '01011*' in getline\
                or '210110' in getline or '011012' in getline\
                or '*10110' in getline or '01101*' in getline\
                or '11001' in getline or '10011' in getline\
                or '10101' in getline or '2011102' in getline\
                or '*011102' in getline or '201110*' in getline\
                or '*01110*' in getline:
                return 'die3'
            if '011010' in getline or '010110' in getline:
                return 'tiao3'
            if '001100' in getline:
                return 'alive2'
            if '001010' in getline or '010100' in getline\
                or '010010' in getline:
                return 'lowalive2'
            if '211000' in getline or '000112' in getline\
                    or '*11000' in getline or '00011*' in getline\
                    or '210100' in getline or '001012' in getline\
                    or '*10100' in getline or '00101*' in getline\
                    or '210010' in getline or '010012' in getline\
                    or '*10010' in getline or '01001*' in getline\
                    or '10001' in getline:
                return 'die2'
            else:
                return 'nothreat'

        # 判断对方棋型
        def judgeType2(getline):
            if '22222' in getline:
                return 'win5'
            if '022220' in getline:
                return 'alive4'
            if '122220' in getline or '022221' in getline\
                    or '*22220' in getline or '02222*' in getline:
                return 'die4'
            if '22202' in getline or '20222' in getline\
                or '22022' in getline:
                return 'lowdie4'
            if '002220' in getline or '022200' in getline:
                return 'alive3'
            if '122200' in getline or '002221' in getline\
                or '*22200' in getline or '00222*' in getline\
                or '122020' in getline or '020221' in getline\
                or '*22020' in getline or '02022*' in getline\
                or '120220' in getline or '022021' in getline\
                or '*20220' in getline or '02202*' in getline\
                or '22002' in getline or '20022' in getline\
                or '20202' in getline or '1022201' in getline\
                or '*022201' in getline or '102220*' in getline\
                or '*02220*' in getline:
                return 'die3'
            if '022020' in getline or '020220' in getline:
                return 'tiao3'
            if '002200' in getline:
                return 'alive2'
            if '002020' in getline or '020200' in getline\
                or '020020' in getline:
                return 'lowalive2'
            if '122000' in getline or '000221' in getline\
                    or '*22000' in getline or '00022*' in getline\
                    or '120200' in getline or '002021' in getline\
                    or '*20200' in getline or '00202*' in getline\
                    or '120020' in getline or '020021' in getline\
                    or '*20020' in getline or '02002*' in getline\
                    or '20002' in getline:
                return 'die2'
            else:
                return 'nothreat'

        # 计算我方形势分数
        def evaluate_self(table):
            row, col = table.shape
            myscore = 0
            for i in range(row):
                for j in range(col):
                    if table[i, j] == 1:
                        point = (i, j)
                        myType={'win5':0, 'alive4':0, 'die4':0, 'lowdie4':0, 'alive3':0, 'die3':0, 'tiao3':0, 'alive2':0, \
                                'lowalive2':0, 'die2':0, 'nothreat':0}
                        lines = getstring(point)
                        for item0 in lines:
                            tmp1 = judgeType1(item0)
                            myType[tmp1] += 1
                        # my score
                        myscore += 1000000*myType['win5']+100000*myType['alive4']+ \
                                   80000 * myType['die4']+70000*myType['lowdie4']+ \
                                   10000 * myType['alive3']+9000*myType['tiao3']+ \
                                   600 * myType['die3']+850*myType['alive2']+ \
                                   100 * myType['lowalive2']+10*myType['die2']+ \
                                   2 * myType['nothreat']
            return myscore

        # 计算敌方的形势分数
        def evaluate_op(table):
            row, col = table.shape
            opscore = 0
            for i in range(row):
                for j in range(col):
                    if table[i, j] == 2:
                        point = (i, j)
                        opType = {'win5': 0, 'alive4': 0, 'die4': 0, 'lowdie4': 0, 'alive3': 0, 'die3': 0, 'tiao3': 0, \
                                  'alive2': 0, 'lowalive2': 0, 'die2': 0, 'nothreat': 0}
                        lines = getstring(point)
                        for item0 in lines:
                            tmp2 = judgeType2(item0)
                            opType[tmp2] += 1
                        # opponent score
                        opscore += 1000000 * opType['win5'] + 300000 * opType['alive4'] + \
                                   200000 * opType['die4'] + 200000 * opType['lowdie4'] + \
                                   50000 * opType['alive3'] + 45000 * opType['tiao3'] + \
                                   600 * opType['die3'] + 750 * opType['alive2'] + \
                                   50 * opType['lowalive2'] + 10 * opType['die2'] + \
                                   1 * opType['nothreat']
            return opscore

        scoretable={}
        defend = 2
        for i in range(row):
            for j in range(col):
                if table[i, j] == 0:
                    #old = evaluate_self(table)-defend*evaluate_op(table)
                    table[i, j] = 1
                    scoretable[(i, j)] = evaluate_self(table)-defend*evaluate_op(table)
                    table[i, j] = 0
        self_position = max(scoretable.items(), key=lambda x: x[1])[0]
        return (self_position[0]+1, self_position[1]+1)


    board, last_move, playing, board_size = state
    row = board_size
    col = board_size
    if len(board[0]) == 0 and len(board[1]) == 0:
        return (board_size/2 + 1, board_size/2 + 1)
    elif len(board[0])+len(board[1]) <= 8:
        return old_evaluation_function(state)
    else:
        return new_evaluation_function(state)

def finish():
    pass
