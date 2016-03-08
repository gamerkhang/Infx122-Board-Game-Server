
class Protocol:

    @staticmethod
    def login(username: str) -> str:
        return "LOGIN@" + username

    @staticmethod
    def new_user(username: str) -> str:
        return "NEW_USER@" + username

    @staticmethod
    def new_game(username: str, game: str) -> str:
        return "NEW_GAME@" + username + "@" + game

    @staticmethod
    def auto_player(username: str) -> str:
        return "AUTO@" + username

    @staticmethod
    def list_of_players(thelist: str) -> str:
        return thelist

    @staticmethod
    def select_player(username : str, player: str) -> str:
        return "LIST@" + username + "@" + player

    @staticmethod
    def send_list(username: str) -> str:
        return "SEND_LIST@" + username

    @staticmethod
    def play_game(game_id: str, move: str):
        return "PLAY@" + game_id + "@" + move
