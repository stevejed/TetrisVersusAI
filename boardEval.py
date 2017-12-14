import board

# Evaluates the game board according to three measures:
#  > Column Heights - Takes the sum of how tall each
#                     column of the board is
#  > Lines Cleared  - Takes the sum of how many lines
#                     were cleared off the board
#  > Gaps           - Takes the sum of the gap slots
#                     of the board that are currently
#                     unable to be filled
#  > Hilly          - Gets the variation in the peaks
#                     of each of the columns
def boardEval(b):
    xSum = 0
    xLines = 0
    xGaps = 0
    xHilly = 0
    
    # Column Heights
    for i in range(b.width):
        j = 0
        while( j < b.height and b.board[j][i] == 0):
            j += 1
        xSum += abs(b.height - j)
    
    # Lines Cleared
    for i in range(b.peak[0],20):
        if b.board[i] == [1,1,1,1,1,1,1,1,1,1]:
            xLines = xLines + 1
    
    # Gaps
    for j in range(10):
        inGap = False
        for i in range(0, 20):
            if b.board[i][j] == 1:
                inGap = True
            if inGap and b.board[i][j] == 0:
                xGaps = xGaps + 1

    # Hilly
    tops = []
    for j in range(b.width):
        i = 0
        while i < b.height-1 and not b.board[i][j] == 1:
            i += 1
        tops.append(i)
    for j in range(b.width-1):
        xHilly += abs(tops[j] - tops[j + 1])

    # Returns the result value
    return b.w[0] * xSum + b.w[1] * xLines + b.w[2] * xGaps + b.w[3] * xHilly
