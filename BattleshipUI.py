import BattleshipBoard


class BattleshipUI:
    
    def setUp(self, player, board):
        self.displayGrid(False,True)
        self.setShip(player, "Carrier", board.get_carrierLength())
        self.displayGrid(False,True)
        self.setShip(player, "Battleship", board.get_battleshipLength())
        self.displayGrid(False,True)
        self.setShip(player, "Submarine", board.get_submarineLength())
        self.displayGrid(False,True)
        self.setShip(player, "Destroyer", board.get_destroyerLength())
        self.displayGrid(False,True)
        self.setShip(player, "Patrol", board.get_patrolLength())

    def setShip(self, player, board, shipType, shipLength):
        while(True):
            try:
                X = int(input("Which column would you like to place the {}(length = {})? ".format(shipType, shipLength)))
                if(not(-1 < X < 11)):
                    print("ERROR: Column out of range")
                    continue
                Y = int(input("Which row would you like to place the {}(length = {})? ".format(shipType, shipLength)))
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


            if (player == '1'):
                cells_clear = False
                if(D == 'H' or D == 'h'):
                    if(X+shipLength > 10):
                        print("ERROR: {} horizontal position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        if(self.primaryGrid1[Y][X+i].getState() == -1):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break
                elif(D == 'V' or D == 'v'):
                    if(Y+shipLength > 10):
                        print("ERROR: {} vertical position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        if(self.primaryGrid1[Y+i][X].getState() == -1):
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
                        if(self.primaryGrid2[Y][X+i].getState() == -1):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break
                elif(D == 'V' or D == 'v'):
                    if(Y+shipLength > 10):
                        print("ERROR: {} vertical position violates grid boundary.".format(shipType))
                        continue
                    for i in range(shipLength):
                        if(self.primaryGrid2[Y+i][X].getState() == -1):
                            print("ERROR: A cell in that position is already taken!")
                            cells_clear = True
                            break

                if(cells_clear):
                    continue
                        
                break                

        if(D == 'H' or D == 'h'):
            for i in range(shipLength):
                if (player == '1'):
                    board.primaryGrid1[Y][X+i] = board._taken
                else:
                    board.primaryGrid2[Y][X+i] = board._taken

        else:
            for i in range(shipLength):
                if (player == '1'):
                    board.primaryGrid1[Y+i][X] = board._taken 
                else:
                    board.primaryGrid2[Y+i][X] = board._taken            

    def displayGrid(self, board, player, tracking, primary):
        if(player == '1'):
            if(tracking):
                print("Tracking Grid")
                for x in range(board.width):
                    print(9-x, board.trackingGrid1[9-x])

            if(primary):
                print("Primary Grid")
                for x in range(board.width):
                    print(9-x, board.primaryGrid1[9-x])
        else:
            if(tracking):
                print("Tracking Grid")
                for x in range(board.width):
                    print(9-x, board.trackingGrid2[9-x])

            if(primary):
                print("Primary Grid")
                for x in range(board.width):
                    print(9-x, board.primaryGrid2[9-x])

    def make_move(self, board):
        while(True):
            try:
                X = int(input("In which column would you like to send the missile? "))
                if(not(-1 < X < 11)):
                    print("ERROR: Column out of range")
                    continue
                Y = int(input("In which row would you like to send the missile? "))
                if(not(-1 < Y < 11)):
                    print("ERROR: Row out of range")
                    continue
                if (not(board.get_tracking_cell_state(board,X,Y) == ' ')):
                    print("ERROR: Attempt already made with that cell.")
                    continue
                break
            except:
                print("ERROR: Invalid input")
                continue
        return X,Y

    def print_scores(board):
        print('************SCORES************')
        print('    1   = {}   &     2   = {} '.format(board.get_score('1'), board.get_score('2')))















    
