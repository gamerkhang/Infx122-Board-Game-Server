
from Board import Board
from GameException import *


class Connect4Board(Board):

    def __init__(self):
        """ Initializes a Connect4 with traditional default values. """
        Board.__init__(self)
        self._NONE = ' '
        self._RED = 'R'
        self._YELLOW = 'Y'

        self._BOARD_COLUMNS = 7
        self._BOARD_ROWS = 6

        self._turn = self._RED

        self._WINING = 'M'

        # self.game_state = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', 'W', 'B', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', 'B', 'W', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        self.game_state = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
					   [' ', ' ', ' ', ' ', ' ', ' ', ' '],
					   [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    def get_none(self):
        return self._NONE

    def get_yellow(self):
        return self._YELLOW

    def get_red(self):
        return self._RED

    def get_game_state(self) -> [[str]]:
        """ Returns the current game state (board). """

        return self.game_state

    def get_num_rows(self) -> int:
        """ Returns the current number of board's rows. """

        return self._BOARD_ROWS

    def get_num_columns(self) -> int:
        """ Returns the current number of board's columns. """

        return self._BOARD_COLUMNS

    def set_num_rows(self, row: str) -> None:
        """ Take an integer as a parameter and set it to the number of rows.
            Method will raise an exception if the parameter is problematic
            for game logic and class. """

        if (4 <= row <= 16) and (row % 2 == 0) and (type(row) == int):

            self._BOARD_ROWS = row

        else:

            raise InvalidInputException()

    def set_num_columns(self, col: int) -> None:
        """ Take an integer as a parameter and set it to the number of columns.
            Method will raise an exception if the parameter is problematic
            for game logic and class.  """

        if (4 <= col <= 16) and (col % 2 == 0) and (type(col) == int):

            self._BOARD_COLUMNS = col

        else:

            raise InvalidInputException()

    def set_first_player(self, user_input: str) -> None:
        """ Take an string as a parameter and set it to the first player turn.
            Method will raise an exception if the parameter is problematic
            for game logic and class. """

        if user_input in ['R', 'Y']:

            self._turn = user_input

        else:

            raise InvalidInputException()

    def set_player_turn(self, player: str) -> None:

        self._turn = player

    def get_player_turn(self) -> str:
        """ Returns the current player turn. """

        return self._turn

    def get_next_player(self) ->str:

        if self._turn == self._YELLOW:

            return self._RED

        return self._YELLOW

    # def get_score(self, player: str) -> int:
        # """ Will the take a string representing a player ('B' for black and 'W' for White)
            # and will return the that players. """

        # count = 0

        # for row in range(self._BOARD_ROWS):
            # for col in range(self._BOARD_COLUMNS):
                # if self.game_state[row][col] == player:
                    # count += 1

        # return count

    def winning_player(self) -> str:
        '''
        Determines the winning player in the given game state, if any.
        If the red player has won, RED is returned; if the yellow player
        has won, YELLOW is returned; if no player has won yet, None is
        returned.
        '''
        winner = None
        for row in range(self._BOARD_ROWS):
            for col in range(self._BOARD_COLUMNS):
                if self._winning_sequence_begins_at(col, row):
                    if winner == None:
                        winner = self.game_state[row][col]
                    elif winner != self.game_state[row][col]:
                        # This handles the rare case of popping a piece
                        # causing both players to have four in a row;
                        # in that case, the last player to make a move
                        # is the winner.
                        return self.get_player_turn() + " wins!"
        if winner != None:
            return winner + " wins!"
        return 'Tie!'

    def _winning_sequence_begins_at(self, col: int, row: int) -> bool:
        '''
        Returns True if a winning sequence of pieces appears on the board
        beginning in the given column and row and extending in any of the
        eight possible directions; returns False otherwise
        '''
        return self._four_in_a_row(col, row, 0, 1) \
                or self._four_in_a_row(col, row, 1, 1) \
                or self._four_in_a_row(col, row, 1, 0) \
                or self._four_in_a_row(col, row, 1, -1) \
                or self._four_in_a_row(col, row, 0, -1) \
                or self._four_in_a_row(col, row, -1, -1) \
                or self._four_in_a_row(col, row, -1, 0) \
                or self._four_in_a_row(col, row, -1, 1)
    
    def _four_in_a_row(self, col: int, row: int, coldelta: int, rowdelta: int) -> bool:
        '''
        Returns True if a winning sequence of pieces appears on the board
        beginning in the given column and row and extending in a direction
        specified by the coldelta and rowdelta
        '''
        start_cell = self.game_state[row][col]

        if start_cell in (None, " "):
            return False
        else:
            for i in range(1, 4):
                if not self._is_valid_column_number(col + coldelta * i) \
                        or not self._is_valid_row_number(row + rowdelta * i) \
                        or self.game_state[row + rowdelta * i][col + coldelta *i] != start_cell:
                    return False
            return True
            
    def _is_valid_column_number(self, column_number: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column_number < self._BOARD_COLUMNS


    def _is_valid_row_number(self, row_number: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise'''
        return 0 <= row_number < self._BOARD_ROWS
    
    def _opposite_turn(self, turn: str) -> str:
        '''Given the player whose turn it is now, returns the opposite player'''
        if turn == RED:
            return YELLOW
        else:
            return RED
        
    def switch_Turn(self) -> None:
        """ This method will change the player's turn. """

        if self._turn == self._RED:
            self._turn = self._YELLOW
        else:
            self._turn = self._RED

