# Solution from Walk-Through
# Path tracing approach

# Start from southwest corner
# Follow a path between hexes, always keeping blue on left
# keep track of all blue stones we pass
# Continue until the east or north side is reached
#   if east side is reached, then blue has a connected path
#   if north side is reached, then blue does not have a connected path


# Optimized Verification
# If connected path exists, repeat the path tracing process from Northwest corner of the board
# Compare blue stone that were tracked in each path
# If any blue stones was passed in both paths, then it could have been the final stone
# Otherwise if intersection is empty, then we have two possible winning paths and the board state is impossible

from copy import deepcopy

DIRECTIONS = [(0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0)]




def count_stones(board):
    nred = 0
    nblue = 0
    n = len(board)

    for i in range(n):
        for j in range(n):
            if board[i][j] == 'R': nred+=1
            elif board[i][j] == 'B': nblue+=1

    return nred, nblue


def pad_board(board, n):

    # Pad top and bottom with Red
    padded_board = ['R' for _ in range(n)] + deepcopy(board) + ['R' for _ in range(n)]

    # Loop through each row and pad ends with Blue
    for r in range(n+2):
        padded_board[r][0] = padded_board[r][-1] = 'B'

    return padded_board

    




def get_next_hex(left, right):
    # Find where the "right hex" is, relative to the "left hex", then return the 
    # "next hex" (in counterclockwise order).
    #
    
    right_dir = (right[0] - left[0], right[1] - left[1])
    for index, direction in enumerate(DIRECTIONS):   
        if right_dir == direction:
            next_dir = DIRECTIONS[(index+1) % 6]
            return (left[0] + next_dir[0], left[1] + next_dir[1])



def step(padded_board, color, left, right):
    
    next_hex = get_next_hex(left, right)
    
    # If Blue -> move Up and to Right
    if padded_board[next_hex[0]][next_hex[1]] == color:
        return next_hex, right
    # If Red -> move Up and to Left
    else:
        return left, next_hex




def blue_path_south(padded_board, m):

    # Two hexes on the last row in in Southwest corner
    left, right = (m-1, 0), (m-1, 1)
    path = set()

    # Follow a path between the hexes, always keeping blue stone on the lft.
    while left[1] < m-1: # Stop when we reach the east side.
        path.add(left)
        left, right = step(padded_board, 'B', left, right)

        if right[0] == 0: # Break if we reach north side
            return None

    return path





def blue_path_north(padded_board, m):
    pass


def red_path_west(padded_board, m):
    pass

def red_path_east(padded_board, m):
    pass


def game_status(n, board):

    num_red, num_blue = count_stones(board)
    if abs(num_red - num_blue) > 1:
        return "Impossible"

    padded_board = pad_board(board, n)
    m = n+2

    south_path = blue_path_south(padded_board, m)
    if south_path:
        north_path = blue_path_north(padded_board, m)
        common_blue_stones = south_path.intersection(north_path)
        if common_blue_stones and num_blue >= num_red:
            return "Blue wins"
        else:
            return "Impossible"

    west_path = red_path_west(padded_board, m)
    if west_path:
        east_path = red_path_east(padded_board, m)
        common_red_stones = west_path.intersection(east_path)
        if common_red_stones and num_red >= num_blue:
            return "Red wins"
        else:
            return "Impossible"

    return "Nobody wins"



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
