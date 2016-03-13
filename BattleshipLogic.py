import BattleshipBoard

class BattleshipLogic:

    # find out how to have the feedback messages on Client side rather than on Server
    # may need to just add some if statements into UI since Board contains ALL GRIDS for both players

    @staticmethod
    def make_move(board, move:[str]):

        row = int(move[0])
        col = int(move[1])
        if (board.get_player_turn() == '1'):
            opponent = '2'
            if (board.get_primary_cell_state(opponent, row, col) == board._taken):
                board.trackingGrid1[row][col] = board._hit
                board.primaryGrid2[row][col] = board._hit
            else:
                board.trackingGrid1[row][col] = board._miss
                board.primaryGrid2[row][col] = board._miss
        else:
            opponent = '1'
            if (board.get_primary_cell_state(opponent, row, col) == board._taken):
                board.trackingGrid2[row][col] = board._hit
                board.primaryGrid1[row][col] = board._hit
            else:
                board.trackingGrid2[row][col] = board._miss
                board.primaryGrid1[row][col] = board._miss

    # double check that winning_player and game_is_over perform as they should 

    @staticmethod
    def winning_player(board):
        if (board.get_score('1') == 0):
            return '2'
        else:
            return '1'

    @staticmethod
    def game_is_over(board):
        if (board.get_score('1') == 0):
            return True
        elif (board.get_score('2') == 0):
            return True
        else:
            return False


    @staticmethod
    def switch_Turn(board):
        if (board.get_player_turn() == '1'):
            board._turn = '2'
        else:
            board._turn = '1'

    @staticmethod
    def all_valid_moves(board):
        return [1,2,3,4,5]
        
        
            
    
