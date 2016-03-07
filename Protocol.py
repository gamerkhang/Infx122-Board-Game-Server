
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
    def list_of_players(username, player):
        return "LIST@" + username + "@" + player


