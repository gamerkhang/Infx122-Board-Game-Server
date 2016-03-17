
class ClientUI:

    @staticmethod
    def get_user_input(prompt_message : str) -> str:
        return input(prompt_message).strip()

    @staticmethod
    def print_detail(message : str) -> None:
        print(message)

    @staticmethod
    def welcome() -> str:
        print("************* Welcome to Board Games *************")

        while True:
            print("l -> Login: ")
            print("c -> Create an account:")
            user_input = input()
            if user_input.upper() not in ["C", "L"]:
                print("Invalid input. Please try it again.")
            else:
                return user_input

    @staticmethod
    def select_game() -> str:
        print("******** Select a Game ********")

        while True:
            print("c -> Connect4 ")
            print("o -> Othello")
            print("b -> Battleship")
            user_input = input()
            if user_input.upper() not in ["C", "O", "B"]:
                print("Invalid input. Please try it again.")
            else:
                return user_input

    @staticmethod
    def select_player() -> str:
        print("******** Select a Player ********")

        while True:
            print("a -> Auto-Selection ")
            print("l -> Select from the list of players")
            user_input = input()
            if user_input.upper() not in ["A", "L"]:
                print("Invalid input. Please try it again.")
            else:
                return user_input

