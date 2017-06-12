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
    # 获取改点4个方向的棋型
    def getstring(point):
        x = point[0]
        y = point[1]
        # vertical
        getLine1 = ''
        for k in range(max(x - 4, 0), min(x + 5, 15)):
            getLine1 += str(int(table[k, y]))
        # horizonal
        getLine2 = ''
        for k in range(max(y - 4, 0), min(y + 5, 15)):
            getLine2 += str(int(table[x, k]))
        # Oblique 45
        getLine3 = ''
        bx = max(0, x - 4)
        by = max(0, y - 4)
        ux = min(14, x + 4)
        uy = min(14, y + 4)
        for k in range(max(bx - x, by - y), min(ux - x, uy - y)+1):
            getLine3 += str(int(table[x + k, y + k]))
        # Oblique 135
        getLine4 = ''
        for k in range(max(bx - x, y - uy), min(ux - x, y - by)+1):
            getLine4 += str(int(table[x + k, y - k]))

        return [getLine1, getLine2, getLine3, getLine4]

    # 判断我方棋型
    def judgeType1(getline):
        if '11111' in getline:
            return 'win5'
        if '011110' in getline:
            return 'alive4'
        if '211110' in getline or '011112' in getline:
            return 'die4'
        if '11101' in getline or '10111' in getline\
            or '11011' in getline:
            return 'lowdie4'
        if '001110' in getline or '011100' in getline:
            return 'alive3'
        if '2011102' in getline or '211100' in getline \
            or '001112' in getline or '11001' in getline\
            or '10011' in getline or '011012' in getline\
            or '210110' in getline or '21101' in getline\
            or '10112' in getline or '10101' in getline\
            or '211001' in getline or '100112' in getline\
            or '10112' in getline or '21101' in getline\
            or '100112' in getline or '211001' in getline:
            return 'die3'
        if '011010' in getline or '010110' in getline:
            return 'tiao3'
        if '001100' in getline:
            return 'alive2'
        if '001010' in getline or '010100' in getline\
            or '010010' in getline:
            return 'lowalive2'
        if '11000' in getline or '00011' in getline:
            return 'die2'
        else:
            return 'nothreat'

    # 判断对方棋型
    def judgeType2(getline):
        if '22222' in getline:
            return 'win5'
        if '022220' in getline:
            return 'alive4'
        if '122220' in getline or '022221' in getline:
            return 'die4'
        if '22202' in getline or '20222' in getline\
            or '22022' in getline:
            return 'lowdie4'
        if '002220' in getline or '022200' in getline:
            return 'alive3'
        if '1022201' in getline or '122200' in getline \
            or '002221' in getline or '22002' in getline\
            or '20022' in getline or '022021' in getline\
            or '120220' in getline or '12202' in getline\
            or '20221' in getline or '20202' in getline\
            or '122002' in getline or '200221' in getline\
            or '20221' in getline or '12202' in getline\
            or '200221' in getline or '122002' in getline:
            return 'die3'
        if '022020' in getline or '020220' in getline:
            return 'tiao3'
        if '002200' in getline:
            return 'alive2'
        if '002020' in getline or '020200' in getline\
            or '020020' in getline:
            return 'lowalive2'
        if '22000' in getline or '00022' in getline:
            return 'die2'
        else:
            return 'nothreat'

    # 计算我方形式分数
    def evaluate_self(table):
        row, col = table.shape
        myscore = 0
        for i in range(row):
            for j in range(col):
                if table[i, j] == 1:
                    point = (i, j)
                    myType={'win5':0, 'alive4':0, 'die4':0, 'lowdie4':0, 'alive3':0, 'die3':0, 'tiao3':0, 'alive2':0, 'lowalive2':0, 'die2':0, 'nothreat':0}
                    lines = getstring(point)
                    for item0 in lines:
                        tmp1 = judgeType1(item0)
                        myType[tmp1] += 1
                    # my score
                    # 赢5
                    if myType['win5']>=1:
                        myscore+=100000
                    # 活4 双死4 死4活3
                    elif myType['alive4']>=1 or myType['die4']>=2 or (myType['die4']>=1 and myType['alive3']>=1):
                        myscore+=10000
                    # 双活3
                    elif myType['alive3']>=2:
                        myscore+=5000
                    # 死3高级活3
                    elif myType['die3']>=1 and myType['alive3']>=1:
                        myscore+=1000
                    # 高级死4
                    elif myType['die4']>=1:
                        myscore+=500
                    # 低级死4
                    elif myType['lowdie4']>=1:
                        myscore+=400
                    # 单活3
                    elif myType['alive3']>=1:
                        myscore+=100
                    # 跳活3
                    elif myType['tiao3']>=1:
                        myscore+=90
                    # 双活2
                    elif myType['alive2']>=2:
                        myscore+=50
                    # 活2
                    elif myType['alive2']>=1:
                        myscore+=10
                    # 低级活2
                    elif myType['lowalive2']>=1:
                        myscore+=9
                    # 死3
                    elif myType['die3']>=1:
                        myscore+=5
                    # 死2
                    elif myType['die2']>=1:
                        myscore+=2
                    # 没有威胁
                    else:
                        myscore+=1
        return myscore

    # 计算敌方的形势分数
    def evaluate_op(table):
        row, col = table.shape
        opscore = 0
        for i in range(row):
            for j in range(col):
                if table[i, j] == 2:
                    point = (i, j)
                    opType = {'win5': 0, 'alive4': 0, 'die4': 0, 'lowdie4': 0, 'alive3': 0, 'die3': 0, 'tiao3': 0, 'alive2': 0,
                              'lowalive2': 0, 'die2': 0, 'nothreat': 0}
                    lines = getstring(point)
                    for item0 in lines:
                        tmp2 = judgeType2(item0)
                        opType[tmp2] += 1
                    # opponent score
                    # 赢5
                    if opType['win5'] >= 1:
                        opscore += 100000
                    # 活4 双死4 死4活3
                    elif opType['alive4'] >= 1 or opType['die4'] >= 2 or (opType['die4'] >= 1 and opType['alive3'] >= 1):
                        opscore += 10000
                    # 双活3
                    elif opType['alive3'] >= 2:
                        opscore += 5000
                    # 死3高级活3
                    elif opType['die3'] >= 1 and opType['alive3'] >= 1:
                        opscore += 1000
                    # 高级死4
                    elif opType['die4'] >= 1:
                        opscore += 500
                    # 低级死4
                    elif opType['lowdie4'] >= 1:
                        opscore += 400
                    # 单活3
                    elif opType['alive3'] >= 1:
                        opscore += 100
                    # 跳活3
                    elif opType['tiao3'] >= 1:
                        opscore += 90
                    # 双活2
                    elif opType['alive2'] >= 2:
                        opscore += 50
                    # 活2
                    elif opType['alive2'] >= 1:
                        opscore += 10
                    # 低级活2
                    elif opType['lowalive2'] >= 1:
                        opscore += 9
                    # 死3
                    elif opType['die3'] >= 1:
                        opscore += 5
                    # 死2
                    elif opType['die2'] >= 1:
                        opscore += 2
                    # 没有威胁
                    else:
                        opscore += 1
        return opscore

    # 下棋思路：当前位置为空，计算我方形势分数-敌方形式分数，然后将此位置令成1，再次计算我方形势分数-敌方形式分数。两次相减，即为下该点的分数。遍历所有空点
    scoretable={}
    for i in range(row):
        for j in range(col):
            if table[i, j] == 0:
                old = evaluate_self(table)-evaluate_op(table)
                table[i, j] = 1
                new = evaluate_self(table)-evaluate_op(table)
                scoretable[(i, j)] = new-old
                table[i, j] = 0
    self_position = max(scoretable.items(), key=lambda x: x[1])[0]
    return (self_position[0]+1, self_position[1]+1)

    # 另一种下棋思路：找出我方形势分数的最大值mymaxscore及其对应的位置，找出敌方形势的最大值hismaxscore及其对应的位置。如果mymaxscore>=hismaxscore，则进攻，下我方形势最大值mymaxscore对应的位置
    # 否则，防守，下敌方形势最大值hismaxscore对应的位置。
    '''
    for i in range(row):
        for j in range(col):
            if table[i, j] == 0:
                table[i, j] = 1
                my_scoretable[(i, j)] = evaluate_self(table)
                table[i, j] = 2
                op_scoretable[(i, j)] = evaluate_op(table)
                table[i, j] = 0
    self_value = max(my_scoretable.items(), key=lambda x: x[1])[1]
    op_value = max(op_scoretable.items(), key=lambda x: x[1])[1]
    if self_value >= op_value:
        self_position = max(my_scoretable.items(), key=lambda x: x[1])[0]
        return (self_position[0]+1, self_position[1]+1)
    else:
        op_position = max(op_scoretable.items(), key=lambda x: x[1])[0]
        return (op_position[0]+1, op_position[1]+1)
    '''

def finish():
    pass