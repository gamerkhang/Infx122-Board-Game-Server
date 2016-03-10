import BattleshipBoard

class BattleshipLogic:

    def make_move(board, player, move):
        if (player == '1'):
            opponent = '2'
            if (board.get_primary_cell_state(opponent, move[1], move[2]) == board._taken):
                print("HIT!")
                board.trackingGrid1[move[1]][move[2]] = board._hit
                board.primaryGrid2[move[1]][move[2]] = board._hit
            else:
                print("Miss...")
                board.trackingGrid1[move[1]][move[2]] = board._miss
                board.primaryGrid2[move[1]][move[2]] = board._miss
        else:
            opponent = '1'
            if (board.get_primary_cell_state(opponent, move[1], move[2]) == board._taken):
                print("HIT!")
                board.trackingGrid2[move[1]][move[2]] = board._hit
                board.primaryGrid1[move[1]][move[2]] = board._hit
            else:
                print("Miss...")
                board.trackingGrid2[move[1]][move[2]] = board._miss
                board.primaryGrid1[move[1]][move[2]] = board._miss

    def game_is_over(board):
        if (board.get_score('1') == 0):
            print("PLAYER 2 WINS!!")
            return True
        elif (board.get_score('2') == 0):
            print("PLAYER 1 WINS!!")
            return True
        else:
            return False

    def switch_turn(board):
        board.switch_turn()
        
        
            
    
