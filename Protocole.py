
def login_protocole(username):
    return "LOGIN@" + username

def new_user_protocole(username):
    return "NEW_USER@" + username

def new_game_protocole(username, game):
    return "NEW_GAME@" + username + "@" + game

