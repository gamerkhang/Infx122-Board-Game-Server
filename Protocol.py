
class Protocol:

    @staticmethod
    def login(username):
        return "LOGIN@" + username

    @staticmethod
    def new_user(username):
        return "NEW_USER@" + username

    @staticmethod
    def new_game(username, game):
        return "NEW_GAME@" + username + "@" + game

    @staticmethod
    def auto_player(username):
        return "AUTO@" + username

    @staticmethod
    def list_of_players(thelist):
        return thelist

    @staticmethod
    def select_player(username, player):
        return "LIST@" + username + "@" + player

    @staticmethod
    def send_list(username):
        return "SEND_LIST@" + username

    @staticmethod
    def play_game(game_id, move):
        return "PLAY@" + game_id + "@" + move
