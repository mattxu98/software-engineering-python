""" A fancy tic-tac-toe game for CSSE1001/7030 A1. """
from constants import *

Board = list[list[str]]
Pieces = list[int]
Move = tuple[int, int, int] # (row, column, piece size)


def num_hours() -> float:
    '''
    Inputs: No input
    Outputs 
        Returns expected hours to finish a1 (type float)
    '''
    return 24.0


def generate_initial_pieces(num_pieces: int) -> Pieces:
    '''
    Inputs
        num_pieces: number of pieces (type int)
    Outputs 
        Returns marker sizes from 1 up to and incl num_pieces (type Pieces)
    '''
    return list(range(1, num_pieces+1))


def initial_state() -> Board:
    '''
    Inputs: No input
    Outputs 
        Returns a new board where every cell contains EMPTY (type Board)
    '''
    # List comprehension is used to avoid shallow copy
    return [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]


def place_piece(board: Board, player: str, pieces_available: Pieces, 
                move: Move) -> None:
    '''
    Inputs 
        board: A squared board of cells which may contain pieces (type Board)
        player: A player's name (type string)
        pieces_available: The player's avaiable peices (type Pieces)
        move: Place a piece of (size) on (row, column) on board (type Move)
    Outputs
        Returns None
    '''
    row, col, size = move
    
    if player in [NAUGHT, CROSS]:
        # adding the piece to the position "move" on the board
        board[row][col] = player + str(size)
        
        # remove the piece from "pieces_available"
        pieces_available.remove(size)
    
    return None


def print_game(board: Board, naught_pieces: Pieces, cross_pieces: Pieces
               ) -> None:
    '''
    Inputs
        board: A squared board of cells which may contain pieces (type Board)
        naught_peices: The available peices of player NAUGHT (type Pieces)
        cross_peices: The available peices of player CROSS (type Pieces)
    Outputs
        Prints something; Returns None
    '''
    # Display the players' pieces
    O_pieces = [str(i) for i in naught_pieces]
    X_pieces = [str(i) for i in cross_pieces]
    print("O has:", ', '.join(O_pieces))
    print("X has:", ', '.join(X_pieces))
    print()
    
    # Prepare board display by flattening a 2D board (type Board) to a 1D list
    flattened = [item for sublist in board for item in sublist]
    i = 1
    
    # Display a well-formatted board which has (2 + 2*GRID_SIZE) printed rows  
    while i <= 2 + 2*GRID_SIZE:
        
        # The first row displays the column indices
        if i == 1:
            i += 1
            elements = [EMPTY] + [' ' + str(i) + ' ' for i in \
                                  range(1, GRID_SIZE)]
            elements += [' ' + str(GRID_SIZE)]
            print(''.join(elements))
        
        # The even-indexed rows displays the "---"-formated row splitters
        elif i % 2 == 0:
            i += 1
            print(EMPTY + '-'*GRID_SIZE*3)
        
        # The odd-indexed rows displays the cells where Pieces may be in place
        else:
            i += 1
            row = int((i-1)/2)
            start, end = (row - 1) * GRID_SIZE, row * GRID_SIZE - 1 
            print(f"{row}|", end='')
            for j in range(GRID_SIZE - 1):
                print(f"{flattened[start + j]}|", end='')
            print(f"{flattened[end]}|")
    
    return None


def process_move(move: str) -> Move | None:
    '''
    Inputs
        move: An instruction of a on-board move (type str)
    Outputs
        If move correctly formatted: Returns its (row, column, piece size) 
        ... (type Move)
        Otherwise: Prints something; Returns None
    '''
    row, col, size = move[0], move[2], move[4]
    
    # identify invalid format by length and space/non-space characters             
    if len(move) != 5 or not (all(i != ' ' for i in [row, col, size]) and \
                              move[1] == ' ' and move[3] == ' '):
        print(INVALID_FORMAT_MESSAGE)
    
    # identify invalid rows, columns, or sizes
    elif row not in [str(i) for i in range(1, GRID_SIZE + 1)]:
        print(INVALID_ROW_MESSAGE)
    elif col not in [str(i) for i in range(1, GRID_SIZE + 1)]:
        print(INVALID_COLUMN_MESSAGE)
    elif size not in [str(i) for i in range(1, PIECES_PER_PLAYER + 1)]:
        print(INVALID_SIZE_MESSAGE)
    
    # return Move of valid format after converting it from str to tuple
    else:
        row, col, size = int(row)-1, int(col)-1, int(size)
        return (row, col, size)


def get_player_move() -> Move:
    '''
    Inputs
        No input as parameters
        prompt: User's input indicating a move on-board (type int)
    Outputs
        If prompt is "h" or "H": Prints something and Returns function
        ... get_player_move() (type Move)
        If prompt is format-validated by function process_move(): Returns the 
        ... move (type Move)
        Otherwise: Returns function get_player_move() (type Move)
    '''
    prompt = input("Enter your move: ")
    
    if prompt in ["h", "H"]:
        print(HELP_MESSAGE)
        return get_player_move()
    else:
        # Returns correctly formatted move (type Move) or Prints error message
        # ... for the incorrectly formatted
        if process_move(prompt):
            return process_move(prompt)
        # Re-prompts user for a correctly formatted if current one is incorrect
        else:
            return get_player_move()


def check_move(board: Board, pieces_available: Pieces, move: Move) -> bool:
    '''
    Inputs
        board: A squared board of cells which may contain pieces (type Board)
        pieces_available: The player's avaiable peices (type Pieces)
        move: Place a piece of (size) on (row, column) on board (type Move)
    Outputs
        Whether the move is valid (type bool)
    '''
    row, col, size = move
    
    # A move is valid only when the size is available, and (row, column) is
    # ... empty or containing a smaller piece
    if size in pieces_available and (board[row][col] == EMPTY or 
                                     size > int(board[row][col][-1])):
        return True
    else:
        return False


def check_win(board: Board) -> str | None:
    '''
    Inputs
        board: A squared board of cells which may contain pieces (type Board)
    Outputs
        If there is a winner: Returns winner (type str)
        Otherwise: Returns None
    '''
    # board with cells containing players only, its transpose, its diagnoal,
    # ... and its reverse diagonal
    who = [[cell[0] for cell in row] for row in board]
    who_transpose = [[who[i][j] for i in range(GRID_SIZE)] for j in 
                     range(GRID_SIZE)]
    diag = [who[i][i] for i in range(GRID_SIZE)]
    rev_diag = [who[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)]
    
    # Only in the following cases a winner exists
    winner = None
    
    # Detects if a player occupies the diagonal
    if all(j == diag[0] for j in diag) and diag[0] != ' ':
        winner = diag[0]
    
    # Detects if a player occupies the reverse diagonal
    elif all(k == rev_diag[0] for k in rev_diag) and rev_diag[0] != ' ':
        winner = rev_diag[0]
    else:
        for i in range(GRID_SIZE):
            
            # Detects if a player occupies a row
            if all(m == who[i][0] for m in who[i]) and who[i][0] != ' ':
                winner = who[i][0]
            
            # Detects if a player occupies a column
            elif all(n == who_transpose[i][0] for n in who_transpose[i]) and \
                 who_transpose[i][0] != ' ':
                winner = who_transpose[i][0]
    
    return winner


def check_stalemate(board: Board, naught_pieces: Pieces, cross_pieces: Pieces
                    ) -> bool:
    '''
    Inputs
        board: A squared board of cells which may contain pieces (type Board)
        naught_peices: The available peices of player NAUGHT (type Pieces)
        cross_peices: The available peices of player CROSS (type Pieces)
    Outputs
        Whether stalemate (no more moves can be made) is reached (type bool)
    '''
    # Extract the piece size of each cell on board
    sizes = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == EMPTY:
                sizes += [0]
            else:
                sizes += [int(board[i][j][-1])]
    
    # Scenarios where no more moves can be made
    # 1. board unfull with min size (0) >= no available pieces (max size = -1)
    # 2. board full with min size (+) >= no available pieces (max size = -1)
    # 3. board full with min size (+) >= max available piece size (+)
    max_naught_peices, max_cross_pieces = -1, -1
    if naught_pieces:
        max_naught_peices = max(naught_pieces)
    if cross_pieces:
        max_cross_pieces = max(cross_pieces)
    
    stalemate = False
    # All the scenarios can be concluded by the same predicate
    if min(sizes) >= max(max_naught_peices, max_cross_pieces):
        stalemate = True
    
    return stalemate


def main() -> None:
    '''
    Inputs: No input
    Outputs: 
        Returns whole_game() (type None)
    '''
    # Helper function covering Step 3, Step 4, Step 5-1
    def test_move(board: Board, player: str, pieces_player: Pieces) -> None:
        '''
        Inputs 
            board: A squared board of cells which may contain pieces(type Board)
            player: A player's name (type string)
            pieces_player: Available pieces of the player (type Pieces)
        Outputs
            If move is correctly formatted and valid: Returns 
            ... place_piece(board, player, pieces_player, move) (type None)
            If move is correctly formatted but invalid: Print something and 
            ... Returns test_move(board, player, pieces_player) (type None)
            Otherwise: Returns test_move(...) (type None)
        '''
        # Step 3: The user is prompted for a move
        move = get_player_move()
        
        # Step 4: Check if the move is correctly formatted and valid
        if move and check_move(board, pieces_player, move):
            # Step 5-1: Update the board
            return place_piece(board, player, pieces_player, move)
        elif move and not check_move(board, pieces_player, move):
            print(INVALID_MOVE_MESSAGE)
            print(f"\n{player} turn to move\n")
            return test_move(board, player, pieces_player)
        else:
            return test_move(board, player, pieces_player)

    # Helper function covering Step 7
    def game_over() -> None:
        '''
        Inputs: No input
        Outputs
            If agree to play again: Returns whole_game() (type: None)
            Otherwise: Returns None
        '''
        # Step 7: Prompt them for whether to play again
        prompt = input("Play again? ")
        if prompt in ["y", "Y"]:
            return whole_game()
        else:
            return None

    # Helper function covering all steps
    def whole_game() -> None:
        '''
        Inputs: No input
        Outputs: Returns None
        '''
        # Initialization of the game
        board = initial_state()
        naught_pieces = generate_initial_pieces(PIECES_PER_PLAYER)
        cross_pieces = generate_initial_pieces(PIECES_PER_PLAYER)
        players = ["O", "X"]
        i = 0

        # Step 1: The current game is displayed
        print_game(board, naught_pieces, cross_pieces)
        
        # Iterate over Step 2 to Step 6
        while check_stalemate(board, naught_pieces, cross_pieces) == False and \
              check_win(board) == None:
            player = players[i % 2]
            if player == "O":
                pieces_player = naught_pieces
            else:
                pieces_player = cross_pieces
            # Step 2: The user is informed whose turn it is to move.
            print(f"\n{player} turn to move\n")
            
            # Step 3, Step 4, Step 5-1
            test_move(board, player, pieces_player)
            i += 1
            
            # Step 5-2: Display the new game state
            print_game(board, naught_pieces, cross_pieces)
            
            # Step 6: Check if the game is over: stalemate or won by someone
            if check_stalemate(board, naught_pieces, cross_pieces) == True:
                print("Stalemate!")
                # Step 7
                game_over()
            elif check_win(board):
                print(check_win(board), "wins!")
                game_over()

    return whole_game()

if __name__ == '__main__':
    main()