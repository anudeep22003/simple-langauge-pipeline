
##### Manual imports ######

from commands import TagCommand
from command_handler import UserCommandHandler
from user import User



class GameInitializer:
    # initialize a user
    
    user_directory = list()
    
    def __init__(self) -> None:
        self.game_orchestrator()
        pass
    
    def game_orchestrator(self):
        
        # create a user
        user = self.create_user()
        self.register_user(user)
        self.start_user_game()
    
    def start_user_game(self):
        for user in self.user_directory:
            self.choose_your_adventure(user)
    
    def choose_your_adventure(self, user: User):
        while True:
            print("what adventure do you want to go on?")
            print("options: (t) Tag\t(d) Delete\t(q) Quit")
            user_input = input("Enter your choice\t---> ")
            if user_input == 't':
                user.command_handler.command_orchestrator(TagCommand)
    
    def create_user(self):
        #name = input("State your name adventurer\t>>  ")
        name = 'Anudeep'
        
        return User(name, id)
        
    def register_user(self, user: User):
        try:
            self.user_directory.append(user)
        except ValueError:
            print("Oops user registration failed")


class SingleUserGameInitializer:
    # initialize a user
    
    user_directory = list()
    
    def __init__(self, game_manager: UserCommandHandler) -> None:
        self.manager = game_manager()
        self.game_orchestrator()
        
        pass
    
    def game_orchestrator(self):
        self.start_game()
    
    def start_game(self):
        self.manager.choose_your_adventure()
        



if __name__ == "__main__":
    game = SingleUserGameInitializer(UserCommandHandler)