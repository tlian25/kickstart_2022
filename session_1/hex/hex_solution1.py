# Solution from Walk-Through
# Flood fill approach
# 
# Slow runtime for multiple checks O(n^4)

from copy import deepcopy


# Hex connected
DIRECTIONS = [(0,-1), (0,1), (1,-1), (1,0), (-1,1), (-1,0)]




def count_stones(board):
    nred = 0
    nblue = 0
    n = len(board)

    for i in range(n):
        for j in range(n):
            if board[i][j] == 'R': nred+=1
            elif board[i][j] == 'B': nblue+=1

    return nred, nblue



# Recursive flooding
def flood(board, row, col, n, color):
    # Set to color
    board[row][col] = color.lower() # lower to distinguish that we saw this cell?

    # Look at immediate neighbors
    for direction in DIRECTIONS:
        new_row, new_col = row + direction[0], col + direction[1]
        if 0 <= new_row < n and 0 <= new_col < n:
            if board[new_row][new_col] == color:
                flood(board, new_row, new_col, n, color)



def check_winner(board, n):

    # Flood fill
    for i in range(n):
        # Flood starting from left border for B
        if board[i][0] == 'B':
            flood(board, i, 0, n, 'B')

        # Flood starting from top border for A
        if board[0][i] == 'R':
            flood(board, 0, i, n, 'R')

    # Check for a winner
    for i in range(n):
        # Check on right side if flood fill reached for B
        if board[i][n-1] == 'b': # lowercase to indicate reached by floodfill
            return 'B'

        # Check on bottom side if flood fill reached for A
        if board[n-1][i] == 'r':
            return 'R'

    return '.'



def game_status(n, original_board):

    num_red, num_blue = count_stones(original_board)
    if abs(num_red - num_blue) > 1:
        return "Impossible"

    board = deepcopy(original_board)
    winner = check_winner(board, n) # will modify board in place
    
    if winner == '.':
        return "Nobody wins"

    if (winner == 'B' and num_blue < num_red) or \
        (winner == 'R' and num_red < num_blue):
        return "Impossible"

    
    # We have a winner
    # need to check winning player could have played the final move
    for r in range(n):
        for c in range(n):
            if original_board[r][c] == winner:

                # Verify that winning player could have played final move
                board = deepcopy(original_board)

                # If we delete this arbitrary move from winner, we expect to see no winner
                board[r][c] = '.'

                # Which is this check below. 
                # Removing the arbitrary move from winner means we should see no winner now
                if check_winner(board, n) == '.':

                    # If the above is true, then we have verified a legitimate win
                    if winner == 'B':
                        return "Blue wins"
                    elif winner == 'R':
                        return "Red wins"

    return "Impossible"




def main():
  test_cases = int(input())
  for test_case in range(1, test_cases + 1, 1):
    board_size = int(input())
    board = []
    for _ in range(board_size):
      board.append(list(input().strip()))

    ans = game_status(board_size, board)

    print("Case #{}: {}".format(test_case, ans))

if __name__ == "__main__":
  main()
