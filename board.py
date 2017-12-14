import random
import math
import copy
class Board:
    def __init__(self):
        # Sets up the board
        self.width = 10
        self.height = 20
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.player = True
        
        # Stores the weight values for the evaluation factors
        self.w = [-.5, .76, -.35, -.18]

        # Stores the last move made on the board
        self.lastMove = [self.height-1,0]

        # Stores the top-most available space
        self.peak = [self.height-1,0]

        # Stores the tetrominos' rotations as lists of indices from the
        # top-left corner of the shape
        self.T = [[[0,0],[1,0],[1,1],[2,0]],
                  [[0,1],[1,0],[1,1],[1,2]],
                  [[0,1],[1,0],[1,1],[2,1]],
                  [[0,0],[0,1],[0,2],[1,1]]]
        
        self.J =[[[0,0],[0,1],[1,0],[2,0]],
                 [[0,0],[1,0],[1,1],[1,2]],
                 [[0,1],[1,1],[2,0],[2,1]],
                 [[0,0],[0,1],[0,2],[1,2]]]

        self.L = [[[0,0],[1,0],[2,0],[2,1]],
                  [[0,2],[1,0],[1,1],[1,2]],
                  [[0,0],[0,1],[1,1],[2,1]],
                  [[0,0],[0,1],[0,2],[1,0]]]
        
        self.O = [[[0,0],[0,1],[1,0],[1,1]]]

        self.Z = [[[0,1],[1,0],[1,1],[2,0]],
                  [[0,0],[0,1],[1,1],[1,2]]]

        self.I = [[[0,0],[1,0],[2,0],[3,0]],
                  [[0,0],[0,1],[0,2],[0,3]]]

        self.S = [[[0,0],[1,0],[1,1],[2,1]],
                  [[0,1],[0,2],[1,0],[1,1]]]
 
        # Stores the possible tetrominos
        self.blocks = [self.T,self.J,self.L,self.O,self.S,self.Z,self.I]

        # Sets up the move queue
        self.queueSize = 2
        self.queue = []
        for i in range(self.queueSize):
            self.queue.append(random.randint(0,len(self.blocks)-1))
            
    # Adds a new random block to the queue
    def generateNextMove(self):
        self.queue.pop(0)
        self.queue.append(random.randint(0,len(self.blocks)-1))

    # Generates possible moves for the given tetromino
    #   > tetromino - int index of the current tetromino
    def generateMoves(self, tetromino):
        moves = []
        
        # Finds the available spaces on the board
        spaces = self.search()
        
        # For the available spaces
        for space in spaces:
            
            # For the current tetromino shape
            shape = self.blocks[tetromino]
            
            # For all rotations of the current tetromino
            for rot in shape:
                
                # Shifts the pivot point up the board until the first
                # available position is found
                pivot = space[0]
                while not(self.validMove(pivot, space[1], rot)):
                    if pivot < 0:
                        break
                    pivot = pivot - 1
                if pivot < 0:
                    break

                # Shifts the block as low as possible and appends it
                # to the set of moves
                moves.append(self.gravDrop(pivot, space[1], rot))

        return moves      

    # Drops the given block as low as is still valid
    #   > pivot - bottom row value of the given block
    #   > col   - left-most column of the given block
    #   > rot   - list of points for the coordinates of the given block
    def gravDrop(self, pivot, col, rot):
        
        # Drops the pivot until it reaches the first invalid move
        while(pivot < self.height-1 and self.validMove(pivot, col, rot)):
            pivot += 1

        # Steps the pivot back one position
        if not self.validMove(pivot, col, rot):
            pivot -= 1

        # Returns the lowest-possible valid move at the given position
        return [(pivot, col),rot]

    # Performs a modified A* search that returns all of the possible moves
    def search(self):
        frontier = []
        explored = []
        spaces = []

        # Adds all of the top-row values that are empty
        for i in range(self.width):
            if self.board[0][i] == 0:
                frontier.append([0,i])

        # Continues to search the frontier while it is not empty
        while(frontier):
            
            # Explores the current position as far as it will go downward
            curr = frontier.pop()
            while(curr[0] < self.height-1 and self.board[curr[0] + 1][curr[1]] == 0):
                explored.append(curr)
                curr[0] += 1

            # Adds the space to explored and spaces (if not already there)
            if curr not in explored:
                explored.append(curr)
            if curr not in spaces:
                spaces.append(curr)

            # Adds all available moves to the left of the current position to the frontier
            for l in range(curr[1]):
                if not self.board[curr[0]][1] == 1:
                    if self.board[curr[0]][l] == 0 and [curr[0],l] not in explored and [curr[0],l] not in frontier:
                        frontier.append([curr[0],l])

            # Adds all available moves to the right of the current position to the frontier
            for r in range(curr[1],self.width):
                if not self.board[curr[0]][r] == 1:
                    if self.board[curr[0]][r] == 0 and [curr[0],r] not in explored and [curr[0],r] not in frontier:
                        frontier.append([curr[0],r])
        return spaces

    # Checks if the given move is valid
    #   > pivot - bottom-left row of the given block
    #   > col   - left-most column of the given block
    #   > rot   - List of coordinates for the current block
    def validMove(self, pivot, col, rot):
        # Gets the max height and width of the block
        h = -1
        w = -1
        for pos in rot:
            if pos[0] > h:
                h = pos[0]
            if pos[1] > w:
                w = pos[1]
        boardPoint = (pivot - h, col)

        # Checks if the piece will be out of bounds
        if pivot < 0 or (col + w) >= self.width:
            return False

        # Checks for collisions of the block's points and its space on the board
        for point in rot:
            if self.board[boardPoint[0] + point[0]][boardPoint[1] + point[1]] == 1:
                return False

        return True

    # Makes the move and updates the board
    #   > move - tuple storing the bottom-left point and block for the move
    def makeMove(self, move):
        self.lastMove = move
        pivot, index = move[0]
        newMove = move[1]

        # Gets the max height of the block
        h = 0
        for pos in newMove:
            if pos[0] > h:
                h = pos[0]
        newpivot = pivot - h

        # Updates the board with the current block
        for pos in newMove:
            if newpivot + pos[0] < self.peak[0]:
                self.peak = [newpivot - 1, pos[1]]
            self.board[newpivot + pos[0]][index + pos[1]] = 1
        
        self.player = not self.player

        # Adds points for lines cleared
        points = 0
        for i in range(self.height):
            if self.board[i] == [1,1,1,1,1,1,1,1,1,1]:
                del self.board[i]
                self.board = [[0,0,0,0,0,0,0,0,0,0]]+self.board
                points+=10

        # Updates peak to account for any cleared lines
        if self.board[self.peak[0]][self.peak[1]] == 0:
            while(self.peak[0] < self.height and self.board[self.peak[0]][self.peak[1]] == 0):
                self.peak[0] += 1
            self.peak[0] -= 1

        return points

    # Hash function for hashtable
    def hash(self):
        tempHash = 0
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board[0])):
                tempHash += (((i*i+j)*2) << self.board[i][j])
        return tempHash
    
    def print(self):
        return str(self.board)
