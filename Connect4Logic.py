
from GameLogic import GameLogic
from GameException import *
from Connect4Board import Connect4Board


class Connect4Logic(GameLogic):

    # @staticmethod
    # def valid_row(board: Connect4Board, row: int) -> bool:
        # """ Will take the row number and return True if the row number is valid,
            # otherwise, False. """

        # # if (0 <= row < self._BOARD_ROWS):
        # if 0 <= row < board.get_num_rows():

            # return True

        # return False

    @staticmethod
    def valid_col(board: Connect4Board, col: int) -> bool:
        """ Will take the column number and return True if the row number is valid,
            otherwise, False. """

        # if ( 0 <= col < self._BOARD_COLUMNS ):
        if 0 <= col < board.get_num_columns():

            return True

        return False

    @staticmethod
    def all_valid_moves(board: Connect4Board) -> list:
        """ It will return all valid moves for current player. """

        all_valid_moves = []

        for col in range(board.get_num_columns()):

            for row in range(board.get_num_rows()):
                if (board.get_game_state()[row][col] in (" ", None)):
                    all_valid_moves.append(col+1)
                    break

        return all_valid_moves

    @staticmethod
    def make_move(board: Connect4Board, move:[str]) -> None:
        """ It will take user's move and update the game state. The method will raise
            and exception if the move is not valid."""
        for i in move:
            print(i)
            
        row = int(move[0])
        col = int(move[1])

        if ((col+1) not in Connect4Logic.all_valid_moves(board) or (None in move)):
            raise InvalidInputException()

        board.get_game_state()[row][col] = board.get_player_turn()

    @staticmethod
    def _get_valid_row(board: Connect4Board, col: int) -> None:
         for row in range(board.get_num_rows()):
            if (board.get_game_state()[board.get_num_rows() - row - 1][col] in (" ", None)):
                return board.get_num_rows() - row - 1
                    

    @staticmethod
    def game_is_over(board: Connect4Board) -> bool:
        """ Will check if the game is over and return True if the game is over
            if there is no move for current and next player, otherwise False. """
        
        return Connect4Logic.all_valid_moves(board) == [] or board.winning_player() != 'Tie!'

    # @staticmethod
    # def _switch_Turn(board: Connect4Board) -> str:
        # """ Return the next player's turn. """

        # if board.get_player_turn() == board.get_black():

            # return board.get_white()

        # return board.get_black()

    @staticmethod
    def switch_Turn(board: Connect4Board) -> None:
        """ This method will change the player's turn. """

        if board.get_player_turn() == board.get_red():

            board.set_player_turn(board.get_yellow())
        else:
            board.set_player_turn(board.get_red())



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

