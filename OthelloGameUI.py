
from GameUI import GameUI
from OthelloBoard import OthelloBoard
from GameException import *

class OthelloGameUI(GameUI):

    @staticmethod
    def make_move(board: OthelloBoard) -> "(row, col)":
        """ It will take an object of class Othello and promote the user for his/her
        move and make the move. """

        while True:

            try:

                print('\nPlease Specify your move. Enter the number of row and columns of a cell on the board.')
                print('-'*85)

                row = OthelloGameUI.move_row(board)
                col = OthelloGameUI.move_col(board)

                return row, col

                break

            except:
                print('\nInvalid move!!!')
                print('Please try it again.')

    @staticmethod
    def move_row(board: OthelloBoard) -> int:
        """ It will take an object of class Othello and promote the user for the
        the row number of his/her move and return it. """

        while True:

            try:

                user_input = (int(input('Please specify the ROW number.\nPlease enter an integer between 1 to {} for number of the row: '.format(board.get_num_rows())))) - 1

                #if game_state.valid_row(user_input):
                if 0 <= user_input < board.get_num_rows():
                    return user_input

                else:

                    raise InvalidInputException()

            except:

                print('\nInvalid Input!!!')
                print('Please try it again.\n')

    @staticmethod
    def move_col(board: OthelloBoard) -> int:
        """ It will take an object of class Othello and promote the user for the
            the column number of his/her move and return it. """

        while True:

            try:

                user_input = (int(input('Please specify the COLUMN number.\nPlease enter an integer between 1 to {} for number of the column: '.format(board.get_num_columns())))) - 1

                #if game_state.valid_col(user_input):
                if 0 <= user_input < board.get_num_columns():

                    return user_input

                else:

                    raise InvalidInputException()

            except:

                print('\nInvalid Input!!!')
                print('Please try it again.\n')

    @staticmethod
    def print_scores(board: OthelloBoard) -> None:
        """ It will print scores of players. """

        print('\n******************************')
        print('************SCORES************')
        print('******************************')
        print('  BLACK = {}   &   WHITE = {} '.format(board.get_score('B'), board.get_score('W')))
        print('******************************\n')

    @staticmethod
    def print_board(board: OthelloBoard) -> None:
        """ It will print the current board. """

        h_line = '   ' + ' ---' * board.get_num_columns() + ' '

        col_num = '  '

        if (board.get_num_columns()/2) < 5:
            for i in range(board.get_num_columns()):
                col_num += '   ' + str(i+1)
        else:
            for i in range(8):
                col_num += '   ' + str(i+1)
            col_num += ' '
            for j in range(8, board.get_num_columns()):
                col_num += '  ' + str(j+1)

        print(col_num)
        print(h_line)

        for i in range(board.get_num_rows()):
            print('{:2d}'.format(i+1), end=' ')
            for j in range(board.get_num_columns()):
                print('| {} '.format(board.get_game_state()[i][j]), end='')
            print('|')
            print(h_line)

    @staticmethod
    def print_winner(winner: str) -> None:
        print(winner)

    @staticmethod
    def print_turn(board: OthelloBoard) -> None:
        """It will print current player. """

        if board.get_player_turn() == board.get_black():
            print('\nBLACK\'s Turn.')
        else:
            print('\nWHITE\'s Turn.')
