import board
import boardEval
import copy

#--------------------
# Points Search
#--------------------
# Iterative-deepening search over the queue of blocks that then returns
# the value of the best board

# Root function for recursion of the points search
#   > alreadySeen - Hashtable that holds the values of previously
#                   explored board states
#   > b           - Board object
#   > queue       - array holding the board's queue of given tetrominos
def points(alreadySeen, b, queue):

    # Helper function for recursion of points search
    #  > b     - Board object
    #  > queue - array holding the board's queue of given tetrominos
    #  > index - int corresponding to the current queue index
    def points_helper(b, queue, index):
        returnval = alreadySeen.get(b.hash())
        if returnval:
            return returnval
        # Evaluates the current board
        value = boardEval.boardEval(b)
    
        # Terminal node
        if len(queue) == index:
            return (value, -1)

        # If no more moves available, then this is a terminal state
        moves = b.generateMoves(queue[index])
        if len(moves) == 0:
            return (value,-1)

        # Otherwise, expands and gets the best move, based on value
        bestMax = -float('inf')
        bestMove = -1
        for move in moves:
            c = copy.deepcopy(b)
            points = c.makeMove(move)
            val,newMove = points_helper(c, queue, index + 1)
            if val> bestMax:
                bestMax = val
                bestMove = move
        returnval = (bestMax, bestMove)
        alreadySeen[b.hash()] = returnval
        return returnval   

    # Iteratively deepens through queue to find the deepest evaluation
    # possible
    bestMove = False
    for i in range(len(queue)):
        tempQ = copy.deepcopy(queue[0:i+1])
        testMove = points_helper(b, tempQ, 0)[1]
        if testMove == -1:
            return bestMove
        else:
            bestMove = testMove
    return bestMove

#--------------------
# Blocks Search
#--------------------
# Iterative-deepening search over the queue of blocks that then returns
# the value of the worst board (thereby, impeding the other player from
# making points)

# Root function for recursion of the block search
#   > alreadySeen - Hashtable that holds the values of previously
#                   explored board states
#   > b           - Board object
#   > queue       - array holding the board's queue of given tetrominos
def blocks(alreadySeen,b, queue):

    # Helper function for recursion of block search
    #  > b     - Board object
    #  > queue - array holding the board's queue of given tetrominos
    #  > index - int corresponding to the current queue index
    def blocks_helper(b, queue, index):
        returnval = alreadySeen.get(b.hash())
        if returnval:
            return returnval        
        # Evaluates the current board
        value = boardEval.boardEval(b)
        
        #Terminal node
        if len(queue) == index:
            return (value, -1)

        #If no more moves available, then this is a terminal state
        moves = b.generateMoves(queue[index])
        if len(moves) == 0:
            return (value,-1)

        # Otherwise, expands and gets the worst move, based on value
        bestMin = float('inf')
        bestMove = -1
        for move in moves:
            c = copy.deepcopy(b)
            points = c.makeMove(move)
            val,newMove = blocks_helper(c, queue, index + 1)
            if val< bestMin:
                bestMin = val
                bestMove = move
        returnval = (bestMin, bestMove) 
        alreadySeen[b.hash()] = returnval
        return returnval   

    # Iteratively deepens through queue to find the deepest evaluation
    # possible
    bestMove = False
    for i in range(len(queue)):
        tempQ = copy.deepcopy(queue[0:i+1])
        testMove = blocks_helper(b, tempQ, 0)[1]
        if testMove == -1:
            return bestMove
        else:
            bestMove = testMove
    return bestMove

#--------------------
# PB Search
#--------------------
# Iterative-deepening search over the queue of blocks that then returns
# the value of the best board

# Root function for recursion of the points search
#   > alreadySeen - Hashtable that holds the values of previously
#                   explored board states
#   > b           - Board object
#   > queue       - array holding the board's queue of given tetrominos
def PB(alreadySeen, b, queue,p1,p2,allowedThreshold,pointGoal):

    # Helper function for recursion of points search
    #  > b     - Board object
    #  > queue - array holding the board's queue of given tetrominos
    #  > index - int corresponding to the current queue index
    def PB_helper(b, queue, index,p1,p2,allowedThreshold,pointGoal):
        returnval = alreadySeen.get(b.hash())
        if returnval:
            return returnval
        
        if index % 2 == 1:
            isPlayer1 = False
        else:
            isPlayer1 = True
        
        # Evaluates the current board
        value = boardEval.boardEval(b)
    
        # Terminal node
        if len(queue) == index:
            return (value, -1)

        # If no more moves available, then this is a terminal state
        moves = b.generateMoves(queue[index])
        if len(moves) == 0:
            return (value,-1)

        if isPlayer1 or (not isPlayer1 and p2 >= (pointGoal / 2) and p2 > p1*allowedThreshold):
            # Otherwise, expands and gets the best move, based on value
            bestMax = -float('inf')
            bestMove = -1
            for move in moves:
                c = copy.deepcopy(b)
                points = c.makeMove(move)
                val,newMove = PB_helper(c, queue, index + 1,p1,p2,allowedThreshold,pointGoal)
                if val> bestMax:
                    bestMax = val
                    bestMove = move
            return (bestMax, bestMove)
        else:
            # Otherwise, expands and gets the worst move, based on value
            bestMin = float('inf')
            bestMove = -1
            for move in moves:
                c = copy.deepcopy(b)
                points = c.makeMove(move)
                val,newMove = PB_helper(c, queue, index + 1,p1,p2,allowedThreshold,pointGoal)
                if val< bestMin:
                    bestMin = val
                    bestMove = move
            returnval = (bestMin, bestMove) 
            alreadySeen[b.hash()] = returnval
            return returnval

    # Iteratively deepens through queue to find the deepest evaluation
    # possible
    bestMove = False
    for i in range(len(queue)):
        tempQ = copy.deepcopy(queue[0:i+1])
        testMove = PB_helper(b, tempQ, 0,p1,p2,allowedThreshold,pointGoal)[1]
        if testMove == -1:
            return bestMove
        else:
            bestMove = testMove
    return bestMove
