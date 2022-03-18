### PYTHON IMPORTS ###
from termcolor import cprint, colored

### MANUAL IMPORTS ###
from abstract_factory import Command, CommandHandler
from commands import TagCommand, QuitCommand, KeywordCleanerCommand
from searchbot_command import SearchBotCommander



class TopLevelUserCommandHandler(CommandHandler):
    
    def __init__(self) -> None:
        pass
    
    def orchestrate(self,command: Command):
        command.orchestrate()
        pass
    
    def choose_your_adventure(self):
        while True:
            print("--> what adventure do you want to go on?")
            cprint(self.option_string(),color='grey', on_color='on_white')
            user_input = input("> Enter your choice\t---> ")
            if user_input == 't':
                command = TagCommand()
            elif user_input == 'q':
                command = QuitCommand()
            elif user_input == 'ck':
                command = KeywordCleanerCommand(local_command_handler= KeywordCommandHandler)
            elif user_input == 'e':
                command = SearchBotCommander(local_command_handler=SearchBotCommandHandler)
            else:
                cprint("Invalid choice, try again!", color='grey',on_color='on_yellow')
                self.choose_your_adventure()
            self.orchestrate(command)
    
    def option_string(self):
        return "--> options: e: (e)xplore\tt: (t)ag\tck: (c)lean (k)eywords\tq: (q)uit"
    
    pass


class KeywordCommandHandler(CommandHandler):
    
    def orchestrate(self, command: Command):
        command.orchestrate()
        
    def choose_your_adventure(self):
        while True:
            adventure = self.initialize_game()
            if adventure == 'quit':
                break
            if not adventure:
                adventure = self.initialize_game()
            else: 
                return adventure
            
            
            pass
        
    
    def initialize_game(self):
        cprint("Choose What type of Keywords you want to explore\n", color='red')
        cprint(self.adventure_options(), color='red')
        user_choice = input("---> ")
        if user_choice == 'v':
            return 'VERB'
        if user_choice == 'n':
            return 'NOUN'
        if user_choice == 'adj':
            return 'ADJ'
        if user_choice == 'pn':
            return "ProperNoun"
        if user_choice == 'q':
            return 'quit'
        else: 
            cprint("Invalid choice", color='red', on_color='on_yellow')
            return 0

    def adventure_options(self):
        return """v: (V)erb\tn: (N)oun\tpn: (P)roper (N)noun\t adj: (Adj)ective"""
    

class SearchBotCommandHandler(CommandHandler):
    
    def __init__(self) -> None:
        pass
    
    
    def orchestrate(self, command: Command):
        command.orchestrate()
        
    def user_input_manager(self):
        pass
    
    def choose_your_adventure(self):
        cprint("Choose your path, can I interest you in one of the following:", color = 'red')
        cprint(self.option_string(), color = 'red')
        user_choice = input("---> ")
        if user_choice == 'v':
            return 'VERB'
        if user_choice == 'n':
            return 'NOUN'
        if user_choice == 'adj':
            return 'ADJ'
        if user_choice == 'pn':
            return "ProperNoun"
        if user_choice == 'q':
            return None
        else: 
            cprint("Invalid choice", color='red', on_color='on_yellow')
            return 0
        
        pass
    
    def size_chooser(self):
        while True:
            cprint("Enter page size", color='red')
            user_input_value = input("---> ")
            if user_input_value == 'q':
                val = None
                break
        
            try:
                val = int(user_input_value)
                if val == 0:
                    cprint("Enter value 1 or higher... 0 is not accepted.")
                else:
                    break
            except ValueError:
                cprint(f"Invalid choice.. enter a number greater than 1, try again")
        
        return val
            
    
    
    
    def option_string(self):
        return """v: (V)erb\tn: (N)oun\tpn: (P)roper (N)noun\t adj: (Adj)ective"""

