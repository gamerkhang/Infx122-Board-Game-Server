
from Board import Board
from GameException import *


class OthelloBoard(Board):

    def __init__(self):
        """ Initializes a Othello with traditional default values. """
        Board.__init__(self)
        self._NONE = ' '
        self._BLACK = 'B'
        self._WHITE = 'W'

        self._BOARD_COLUMNS = 8
        self._BOARD_ROWS = 8

        self._turn = self._BLACK

        self._TOP_LEFT = self._WHITE

        self._WINING = 'M'

        self.game_state = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', 'W', 'B', ' ', ' ', ' '],
                           [' ', ' ', ' ', 'B', 'W', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


    def get_none(self):
        return self._NONE

    def get_white(self):
        return self._WHITE

    def get_black(self):
        return self._BLACK

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

        if user_input in ['B', 'W']:

            self._turn = user_input

        else:

            raise InvalidInputException()

    def set_player_turn(self, player: str) -> None:

        self._turn = player

    def get_player_turn(self) -> str:
        """ Returns the current player turn. """

        return self._turn

    def get_next_player(self) ->str:

        if self._turn == self._WHITE:

            return self._BLACK

        return self._WHITE

    def get_score(self, player: str) -> int:
        """ Will the take a string representing a player ('B' for black and 'W' for White)
            and will return the that players. """

        count = 0

        for row in range(self._BOARD_ROWS):
            for col in range(self._BOARD_COLUMNS):
                if self.game_state[row][col] == player:
                    count += 1

        return count

    def winning_player(self) -> str:
        """ Will return a string showing the winner's status if any.
            The method will return no winner, if both players have same scores."""

        white_score = self.get_score(self._WHITE)

        black_score = self.get_score(self._BLACK)

        if self._WINING == 'M':

            if white_score > black_score:

                return 'WINNER is White Player.'

            elif white_score < black_score:

                return 'WINNER is Black Player.'

        elif self._WINING == 'F':

            if white_score < black_score:

                return 'WINNER is White Player.'

            elif white_score > black_score:

                return 'WINNER is Black Player.'

        return 'NO WINNER. Both Players have the same SCORE!!!!'

    def switch_Turn(self) -> None:
        """ This method will change the player's turn. """

        if self._turn == self._BLACK:
            self._turn = self._WHITE
        else:
            self._turn = self._BLACK

