class BattleshipBoard:

    def __init__(self):
        self.carrierLength = 5
        self.battleshipLength = 4
        self.submarineLength = 3
        self.destroyerLength = 3
        self.patrolLength = 2

        self._empty = ' '
        self._taken = 'X'
        self._hit = '!'
        self._miss = '-'
        
        self.width = 10
        self.length = 10

        self._turn = '1'
        
        self.primaryGrid1 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]
        self.primaryGrid2 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]

        self.trackingGrid1 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]
        self.trackingGrid2 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]


     #def get_game_state(): #String[][]
    def get_carrierLength():
        return self.carrierLength

    def get_battleshipLength():
        return self.battleshipLength

    def get_submarineLength():
        return self.submarineLength

    def get_destroyerLength():
        return self.destroyerLength

    def get_patrolLength():
        return self.patrolLength

    def get_num_rows(self):
        return self.length
    
    def get_num_columns(self):
        return self.width

    def set_num_rows(self, row):
        self.length = row

    def set_num_columns(self, col):
        self.width = col

    def get_player_turn(self):
        return self._turn

    def get_next_player(self):
        if (self._turn == '1'):
            return '2'
        else:
            return '1'

    def set_player_turn(self, player):
        self._turn = player

    def switch_turn(self):
        if (self._turn == '1'):
            self._turn = '2'
        else:
            self._turn = '1'


    def get_score(self, player):
        score = self.carrierLength + self.battleshipLength + self.submarineLength + self.destroyerLength+ self.patrolLength
        
        for x in range(self.width):
            for y in range(self.length):
                if (player == '1'):
                    if (self.primaryGrid1[x][y] == '!'):
                        score -= 1
                else:
                    if (self.primaryGrid2[x][y] == '!'):
                        score -= 1
        return score

    def get_tracking_cell_state(self, player, x, y):
        if (player == '1'):
            return self.trackingGrid1[x][y]
        else:
            return self.trackingGrid2[x][y]

    def get_primary_cell_state(self, player, x, y):
        if (player == '1'):
            return self.primaryGrid1[x][y]
        else:
            return self.primaryGrid2[x][y]
        
                        
                    
            
        
        
    
    '''
    def setUp(self):
        self.displayGrid(False,True)
        self.setShip("Carrier", Battleship.carrierLength)
        self.displayGrid(False,True)
        self.setShip("Battleship", Battleship.battleshipLength)
        self.displayGrid(False,True)
        self.setShip("Submarine", Battleship.submarineLength)
        self.displayGrid(False,True)
        self.setShip("Destroyer", Battleship.destroyerLength)
        self.displayGrid(False,True)
        self.setShip("Patrol", Battleship.patrolLength)

    def setShip(self, shipType, shipLength):
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


            cells_clear = False
            if(D == 'H' or D == 'h'):
                if(X+shipLength > 10):
                    print("ERROR: {} horizontal position violates grid boundary.".format(shipType))
                    continue
                for i in range(shipLength):
                    if(self.primaryGrid[Y][X+i].getState() == -1):
                        print("ERROR: A cell in that position is already taken!")
                        cells_clear = True
                        break
            elif(D == 'V' or D == 'v'):
                if(Y+shipLength > 10):
                    print("ERROR: {} vertical position violates grid boundary.".format(shipType))
                    continue
                for i in range(shipLength):
                    if(self.primaryGrid[Y+i][X].getState() == -1):
                        print("ERROR: A cell in that position is already taken!")
                        cells_clear = True
                        break

            if(cells_clear):
                continue
                        
            break

        if(D == 'H' or D == 'h'):
            for i in range(shipLength):
                self.primaryGrid[Y][X+i].activate()
        else:
            for i in range(shipLength):
                self.primaryGrid[Y+i][X].activate()
            
        
    def displayGrid(self,tracking,primary):
        if(tracking):
            print("Tracking Grid")
            for x in range(self.width):
                print(9-x, self.trackingGrid[9-x])

        if(primary):
            print("Primary Grid")
            for x in range(self.width):
                print(9-x, self.primaryGrid[9-x])

    def primaryTouch(self,x,y):
        return self.primaryGrid[x][y].hit()

    def trackingTouch(self,x,y):
        return self.trackingGrid[x][y].hit(True) # or False

    '''

    '''
    class primaryCell:

        def __init__(self,x,y):
            self.x = x
            self.y = y
            # possible Cell states to display:
            #   not selected (store as 0, display as -)
            #   taken (store as -1; display as X)
            #   hit (store as 1; display as !)
            self.state = 0

        def __repr__(self):
            if(self.state == 1):
                return '!'
            elif(self.state == -1):
                return '~'
            else:
                return '-'
            
        def getState(self):
            return self.state

        def activate(self):
            self.state = -1

        def hit(self):
            if(self.state == -1):
                self.state = 1
                return True
            else:
                return False

    class trackingCell:

        def __init__(self,x,y):
            self.x = x
            self.y = y
            # possible states:
            #   not selected (store as 0, display as -)
            #   hit (store as 1; display as !)
            #   miss (store as -1; display as 0)
            self.state = 0

        def __repr__(self):
            if(self.state == 1):
                return '!'
            elif(self.state == -1):
                return '0'
            else:
                return '-'

        def hit(self,result):
            if(result):
                self.state = 1
            else:
                self.state = -1
    '''
