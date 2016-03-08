
from GameLogic import GameLogic
from GameException import *
from OthelloBoard import OthelloBoard


class OthelloLogic(GameLogic):

    @staticmethod
    def valid_row(board: OthelloBoard, row: int) -> bool:
        """ Will take the row number and return True if the row number is valid,
            otherwise, False. """

        # if (0 <= row < self._BOARD_ROWS):
        if 0 <= row < board.get_num_rows():

            return True

        return False

    @staticmethod
    def valid_col(board: OthelloBoard, col: int) -> bool:
        """ Will take the column number and return True if the row number is valid,
            otherwise, False. """

        # if ( 0 <= col < self._BOARD_COLUMNS ):
        if 0 <= col < board.get_num_columns():

            return True

        return False

    @staticmethod
    def valid_moves(board: OthelloBoard, row: int, col: int) -> list:
        """ Take the move (row and col), and return a list of all dices that should be
            flipped with that move. If the list is empty, it means the move is not
            valid."""

        dices_to_flip = []

        if (OthelloLogic.valid_row(row)) and (OthelloLogic.valid_col(col)) and (board.get_game_state()[row][col] != board.get_none()):
            return dices_to_flip

        current_player = board.get_player_turn()
        next_player = OthelloLogic._switch_Turn()

        for [row_coordinates, col_coordinates] in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:

            temp_row = row
            temp_col = col

            temp = [row_coordinates + row, col_coordinates + col]

            if OthelloLogic.valid_row(temp[0]) and OthelloLogic.valid_col(temp[1]) and (board.get_game_state()[temp[0]][temp[1]] == next_player):

                temp = [row_coordinates + temp[0], col_coordinates + temp[1]]

                if not (OthelloLogic.valid_row(temp[0]) and OthelloLogic.valid_col(temp[1])):
                    continue

                while board.get_game_state()[temp[0]][temp[1]] == next_player:

                    temp = [row_coordinates + temp[0], col_coordinates + temp[1]]

                    if not (OthelloLogic.valid_row(temp[0]) and OthelloLogic.valid_col(temp[1])):
                        break

                if not (OthelloLogic.valid_row(temp[0]) and OthelloLogic.valid_col(temp[1])):
                    continue

                if board.get_game_state()[temp[0]][temp[1]] == current_player:

                    while True:

                        temp = [temp[0] - row_coordinates, temp[1] - col_coordinates]
                        if (temp[0] == row) and (temp[1] == col):
                            break
                        dices_to_flip.append(temp)

        return dices_to_flip

    @staticmethod
    def all_valid_moves(board: OthelloBoard) -> list:
        """ It will return all valid moves for curent player. """

        all_valid_moves = []

        for row in range(board.get_num_rows()):

            for col in range(board.get_num_rows()):
                temp = [row, col]
                if len(OthelloLogic.valid_moves(row, col)) != 0:
                    all_valid_moves.append(temp)

        return all_valid_moves

    @staticmethod
    def make_move(board: OthelloBoard, move:[str]) -> None:
        """ It will take user's move and update the game state. The method will raise
            and exception if the move is not valid."""

        row = int(move[0])
        col = int(move[1])

        if (not (OthelloLogic.valid_row(row))) or (not (OthelloLogic.valid_col(col))) or (board.get_game_state()[row][col] != board.get_none()):
            raise InvalidInputException()

        dices_to_flip = OthelloLogic.valid_moves(row, col)

        if len(dices_to_flip) == 0:
            raise InvalidInputException()

        board.get_game_state()[row][col] = board.get_player_turn()

        for index in dices_to_flip:

            board.get_game_state()[index[0]][index[1]] = board.get_player_turn()

    @staticmethod
    def game_is_over(board: OthelloBoard) -> bool:
        """ Will check if the game is over and return True if the game is over
            if there is no move for current and next player, otherwise False. """

        if len(OthelloLogic.all_valid_moves()) != 0:

            return False

        OthelloLogic.switch_Turn()

        if len(OthelloLogic.all_valid_moves()) == 0:

            OthelloLogic.switch_Turn()

            return True

        else:

            OthelloLogic.switch_Turn()

            return False

    @staticmethod
    def _switch_Turn(board: OthelloBoard) -> str:
        """ Return the next player's turn. """

        if board.get_player_turn() == board.get_black():

            return board.get_white()

        return board.get_black()

    @staticmethod
    def switch_Turn(board: OthelloBoard) -> None:
        """ This method will change the player's turn. """

        if board.get_player_turn() == board.get_black():

            board.set_player_turn(board.get_white())
        else:
            board.set_player_turn(board.get_black())



    # def _switch_dice(self) -> None:
    #     """ Will change the dice type. White to black or vice versa. """
    #
    #     if self._TOP_LEFT == self._BLACK:
    #
    #         self._TOP_LEFT = self._WHITE
    #
    #     else:
    #
    #         self._TOP_LEFT = self._BLACK

