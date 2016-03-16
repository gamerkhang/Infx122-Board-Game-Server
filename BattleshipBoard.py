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

        #self.primaryGrid1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        #self.primaryGrid2 = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        self.trackingGrid1 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]
        self.trackingGrid2 = [ [ self._empty for x in range(self.width) ] for y in range(self.length) ]

        #self.trackingGrid1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        #self.trackingGrid2 = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        #                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


    def get_game_state(self): #String[][]
        if (self._turn == '1'):
            return self.primaryGrid1
        if (self._turn == '2'):
            return self.primaryGrid2

    def get_tracking_state(self):
        if (self._turn == '1'):
            return self.trackingGrid1
        if (self._turn == '2'):
            return self.trackingGrid2
        
    def get_carrierLength(self):
        return self.carrierLength

    def get_battleshipLength(self):
        return self.battleshipLength

    def get_submarineLength(self):
        return self.submarineLength

    def get_destroyerLength(self):
        return self.destroyerLength

    def get_patrolLength(self):
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

    def switch_Turn(self):
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
                    if (self.trackingGrid1[x][y] == '!'):
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
        
                        
    def winning_player(self):
        winner = None
        if (self.get_score('1') == 0):
            return "Your opponent won :("
        elif (self.get_score('2') == 0):
            return "YOU WIN!!"
            
        
        
