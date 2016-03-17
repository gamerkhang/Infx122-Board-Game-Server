import BattleshipBoard


class BattleshipGameUI:

    def setUp(self, Board):
        self.setShip(Board, "Carrier", Board.get_carrierLength())
        self.print_board(Board)
        self.setShip(Board, "Battleship", Board.get_battleshipLength())
        self.print_board(Board)
        self.setShip(Board, "Submarine", Board.get_submarineLength())
        self.print_board(Board)
        self.setShip(Board, "Destroyer", Board.get_destroyerLength())
        self.print_board(Board)
        self.setShip(Board, "Patrol", Board.get_patrolLength())
        self.print_board(Board)
        

    def setShip(self, Board, shipType, shipLength):
        while(True):
            try:
                X = int(input("Which column would you like to place the {}(length = {})? ".format(shipType, shipLength))) - 1
                if(not(-1 < X < 11)):
                    print("ERROR: Column out of range")
                    continue
                Y = int(input("Which row would you like to place the {}(length = {})? ".format(shipType, shipLength))) - 1
                if(not(-1 < Y < 11)):
                    print("ERROR: Row out of range")
                    continue
                D = input("Place {} horizontally or vertically (H or V)? ".format(shipType))
                if(not(D == 'H' or D == 'h' or D == 'V' or D == 'v')):
                    print("ERROR: Expecting 'H' or 'V'")
                    continue
            except:
                print("ERROR: Invalid input")
                continue


            if (Board.get_player_turn() == '1'):
                cells_clear = False
                if(D == 'H' or D == 'h'):
                    if(X+shipLength > 10):
                        print("ERROR: {} horizontal position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        #if(Board.primaryGrid1[Y][X+i] == -1):
                        if(Board.primaryGrid1[Y][X+i] == Board._taken):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break
                elif(D == 'V' or D == 'v'):
                    if(Y+shipLength > 10):
                        print("ERROR: {} vertical position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        #if(Board.primaryGrid1[Y+i][X] == -1):
                        if(Board.primaryGrid1[Y][X+i] == Board._taken):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break

                if(cells_clear):
                    continue
                        
                break
            else:
                cells_clear = False
                if(D == 'H' or D == 'h'):
                    if(X+shipLength > 10):
                        print("ERROR: {} horizontal position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        #if(Board.primaryGrid2[Y][X+i]== -1):
                        if(Board.primaryGrid1[Y][X+i] == Board._taken):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break
                elif(D == 'V' or D == 'v'):
                    if(Y+shipLength > 10):
                        print("ERROR: {} vertical position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        #if(Board.primaryGrid2[Y+i][X] == -1):
                        if(Board.primaryGrid1[Y][X+i] == Board._taken):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break

                if(cells_clear):
                    continue
                        
                break                

        if(D == 'H' or D == 'h'):
            for i in range(shipLength):
                if (Board.get_player_turn() == '1'):
                    Board.primaryGrid1[Y][X+i] = Board._taken
                else:
                    Board.primaryGrid2[Y][X+i] = Board._taken

        else:
            for i in range(shipLength):
                if (Board.get_player_turn() == '1'):
                    Board.primaryGrid1[Y+i][X] = Board._taken 
                else:
                    Board.primaryGrid2[Y+i][X] = Board._taken            

    @staticmethod
    def print_board(board):

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


        print("Tracking Grid")
        print(col_num)
        print(h_line)
        for i in range(board.get_num_rows()):
            print('{:2d}'.format(i+1), end=' ')
            for j in range(board.get_num_columns()):
                print('| {} '.format(board.trackingGrid1[j][i]), end='')
            print('|')
            print(h_line)

        print("\nPrimary Grid")
        print(col_num)
        print(h_line)
        for i in range(board.get_num_rows()):
            print('{:2d}'.format(i+1), end=' ')
            for j in range(board.get_num_columns()):
                print('| {} '.format(board.primaryGrid1[i][j]), end='')
            print('|')
            print(h_line)


        

    @staticmethod
    def make_move(Board):
        while(True):
            try:
                X = int(input("In which column would you like to send the missile? ")) - 1
                if(not(-1 < X < 11)):
                    print("ERROR: Column out of range")
                    continue
                Y = int(input("In which row would you like to send the missile? ")) - 1
                if(not(-1 < Y < 11)):
                    print("ERROR: Row out of range")
                    continue
                if (not(Board.get_tracking_cell_state('1',X,Y) == ' ')):
                    print("ERROR: Attempt already made with that cell.")
                    continue
                break
            except:
                print("ERROR: Invalid input")
                continue
        
        return Y,X

    @staticmethod
    def print_scores(Board):
        print('************SCORES************')
        print('   You  = {}  & Opponent = {} '.format(Board.get_score('1'), Board.get_score('2')))

    @staticmethod
    def print_winner(Board):
        if (board.get_score('1') == 0):
            print("GAME OVER!! Player 2 WINS!!!")
        elif (board.get_score('2') == 0):
            print("GAME OVER!! Player 1 WINS!!!")

    @staticmethod
    def print_turn(Board):
        print("It is currently Player {}'s turn.".format(Board.get_player_turn()))















    
