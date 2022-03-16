import imp
from abstract_factory import Command
from commands import TagCommand, QuitCommand, KeywordCleanerCommand
from termcolor import cprint, colored


class UserCommandHandler:
    
    def __init__(self) -> None:
        pass
    
    def orchestrate(self,command: Command):
        command.orchestrate()
        pass
    
    def choose_your_adventure(self):
        while True:
            print("--> what adventure do you want to go on?")
            cprint("--> options: t: (t)ag\tck: (c)lean (k)eywords\tq: (q)uit",color='blue', on_color='on_grey')
            user_input = input("> Enter your choice\t---> ")
            if user_input == 't':
                command = TagCommand()
            if user_input == 'q':
                command = QuitCommand()
            if user_input == 'ck':
                command = KeywordCleanerCommand()
            
            self.orchestrate(command)
    
    pass

