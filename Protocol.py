
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
    def list_match(username: str, player: str) -> str:
        return "LIST_MATCH@" + username + "@" + player

    @staticmethod
    def play_with(username: str, play_with: str) -> str:
        return "PLAY_WITH@" + username + "@" + play_with

    @staticmethod
    def send_list(username: str, game_name: str) -> str:
        return "SEND_LIST@" + username + "@" + game_name

    @staticmethod
    def play_game(game_id: str, move: str):
        return "PLAY@" + game_id + "@" + move
