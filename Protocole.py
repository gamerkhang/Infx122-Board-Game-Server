
def login_protocole(username):
    return "LOGIN@" + username

def new_user_protocole(username):
    return "NEW_USER@" + username

def new_game_protocole(username, game):
    return "NEW_GAME@" + username + "@" + game

def select_auto_player_protocole(username):
    return "AUTO@" + username

def select_list_player_protocole(username,player):
    return "LIST@" + username + "@" + player