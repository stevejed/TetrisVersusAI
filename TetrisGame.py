import board
import boardEval
import moveSearch
import math
import random
class Game:


    def __init__(self, startBoard, player1, player2):
        self.startBoard = startBoard
        self.player1 = player1
        self.player2 = player2
        self.simulateLocalGame()
    ########################################################################
    #                     Simulate a Local Game
    ########################################################################

    def simulateLocalGame(self):

        board = self.startBoard
        isPlayer1 = True
        startTet = []
        p1 = 0
        p2 = 0
        alreadySeen1= {}
        alreadySeen2= {}
        #####################
        #    Modify These
        #********************
        allowedThreshold = 1.35 # Percentage where playerPB switches between blocking
                                # and points (p1 > p2 * allowedThreshold)
                                
        pointGoal = 500         # Point threshold where game is won (line clear = 10)
        #####################

        # Plays the game
        while(True):
            
            #finds the move to make
            if isPlayer1:
                move = self.player1.findMove(alreadySeen1,board,p1,p2,allowedThreshold, pointGoal)
            else:
                move = self.player2.findMove(alreadySeen2,board,p2,p1,allowedThreshold, pointGoal)
            
            # Determines if the game is over or not
            
            # Player 1 won!
            if not move and not isPlayer1 or p1 > pointGoal:
                print(self.player1.name+" wins!")
                print("Last Move Made:"+str(board.lastMove))
                for i in range(len(board.board)):
                    line = "["
                    for j in range(len(board.board[0])):
                        line += str(board.board[i][j])
                    line += "]"
                    print(line)
                print(self.player1.name+" score:" + str(p1))
                print(self.player2.name+" score:" + str(p2))
                break

            # Player 2 won!
            elif not move and isPlayer1 or p2 > pointGoal:
                print(self.player2.name+" wins!")
                print("Last Move Made:"+str(board.lastMove))
                print("**********")
                for i in range(len(board.board)):
                    line = "["
                    for j in range(len(board.board[0])):
                        line += str(board.board[i][j])
                    line += "]"
                    print(line)

                print(self.player1.name+" score:" + str(p1))
                print(self.player2.name+" score:" + str(p2))
                break

            # Makes next move and updates board
            else:
                if isPlayer1:
                    p1 += board.makeMove(move)
                else:
                    p2 += board.makeMove(move)
                board.generateNextMove()
                isPlayer1 = not isPlayer1
                
#********************
#       Players
#********************
# Player that goes after points
class playerPoints:
    def __init__(self):
        self.name = "Player Points"
    def findMove(self,alreadySeen,board,p1,p2,allowedThreshold, pointGoal):
        return moveSearch.points(alreadySeen,board,board.queue)

# Player that goes for blocking its opponent
class playerBlocks:
    def __init__(self):
        self.name = "Player Blocks"
    def findMove(self,alreadySeen,board,p1,p2,allowedThreshold, pointGoal):
        return moveSearch.blocks(alreadySeen,board,board.queue)

# Player that goes for either points or blocking its opponent according
# to the provided threshold
class playerPB:
    def __init__(self):
        self.name = "Player going for points and blocks"
    def findMove(self,alreadySeen,board,p1,p2,allowedThreshold, pointGoal):
##        if p1 > p2*allowedThreshold:
##            return moveSearch.blocks(alreadySeen,board,board.queue)
##        else:
##            return moveSearch.points(alreadySeen,board,board.queue)
        return moveSearch.PB(alreadySeen,board,board.queue,p1,p2,allowedThreshold,pointGoal)

# Player that randomly selects from the available moves
class playerRandom:
    def __init__(self):
        self.name = "Randy"
    def findMove(self,alreadySeen,board,p1,p2,allowedThreshold, pointGoal):
        moves = board.generateMoves(board.queue[0])
        if len(moves) == 0:
            return False
        return random.choice(moves)

###############################
#     Select Players Here
#******************************
#  > For Points... playerPoints()
#  > For Blocks... playerBlocks()
#  > For Both...   playerPB()
#  > For Random... playerRandom()

g = Game(board.Board(),playerPoints(),playerPB())
