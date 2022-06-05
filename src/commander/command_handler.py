### PYTHON IMPORTS ###
from ast import Call
from typing import Callable
from matplotlib import use
from numpy import size
from termcolor import cprint, colored
from tabulate import tabulate


### MANUAL IMPORTS ###
from abstract_factory import Command, CommandHandler
from commands import TagCommand, QuitCommand, KeywordCleanerCommand
from searchbot_command import SearchBotCommander
from enum_factory import AdventureOptions,PrintColors


class TopLevelUserCommandHandler(CommandHandler):
    
    def __init__(self) -> None:
        pass
    
    def orchestrate(self,command: Command):
        command.orchestrate()
        pass
    
    def choose_your_adventure(self):
        while True:
            print("--> what adventure do you want to go on?")
            cprint(self.option_string(), color = PrintColors.system_prompt_text.value, on_color = PrintColors.system_prompt_on.value)
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
                cprint("Invalid choice, try again!", color = PrintColors.system_prompt_text.value,on_color=PrintColors.error_on.value)
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
        cprint("Choose What type of Keywords you want to explore\n", color=PrintColors.system.value)
        cprint(self.adventure_options(), color=PrintColors.system.value)
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
            cprint("Invalid choice", color=PrintColors.system.value, on_color=PrintColors.error_on.value)
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
    
    def choose_your_adventure(self) -> AdventureOptions:
        while True:
            cprint("Choose your path, can I interest you in one of the following:", color = 'red')
            cprint(self.option_string(), color = 'red')
            user_choice = input("---> ")
            if user_choice == 'q':
                return AdventureOptions.quit
            elif user_choice == 'v':
                return AdventureOptions.VERB
            elif user_choice == 'n':
                return AdventureOptions.NOUN
            elif user_choice == 'adj':
                return AdventureOptions.ADJ
            elif user_choice == 'pn':
                return AdventureOptions.ProperNoun
            else: 
                cprint("Invalid choice", color=PrintColors.system.value, on_color=PrintColors.error_on.value)    
    
    def size_chooser(self, adventure_choice: AdventureOptions):
        while True:
            if adventure_choice.value is None:
                return None
            else:
                cprint("Enter page size", color=PrintColors.system.value)
                user_input_value = input("---> ")

            if user_input_value == 'q':
                return None
            try:
                val = int(user_input_value)
                if val == 0:
                    cprint("Enter value 1 or higher... 0 is not accepted.")
                else:
                    return val
            except ValueError:
                cprint(f"Invalid choice.. enter a number greater than 1, try again")
    
    def user_input_orchestrator(self):
        # get the user to choose their adventure 
        # get them to choose a size (optional really leave the default at 50)    
        
        adventure = self.choose_your_adventure()
        size = self.size_chooser(adventure)
        
        return size, adventure
            
    def get_user_keyword_choices_older(self, 
                                 available_keyword_options: list,
                                 adventure: AdventureOptions,
                                 option_builder_fn: Callable):
        # take available keyword choices
        # convert into a table ready format 
        # display to user
        # take input
                # --> show contextual choices
        # ask if they want to make more input 
        # return the selected choices, adventure
        user_selection_final = list()
        while True:
            print(tabulate(self.list_to_table_formatter(available_keyword_options)))
            user_index_selection = self.select_index_of_choices()
            
            if user_index_selection is None:
                return None
            
            user_selection = [(available_keyword_options[index]['keyword'], f">{available_keyword_options[index]['count']}<")
                              for index in user_index_selection]
            
            cprint("You selected the following: ", color = PrintColors.system.value)
            print(user_selection)
            cprint(self.option_string(purpose='index_selection'), color=PrintColors.system.value)
            response = input("--> ")
            while True:
                    if response == 'c':
                        user_selection_final.extend([word for word,_ in user_selection])
                        cprint("completed selection:", color=PrintColors.system.value)
                        print(user_selection_final)
                        return user_selection_final
                    elif response == 'a':
                        cprint("selection so far...", color=PrintColors.system.value)
                        user_selection_final.extend([word for word,_ in user_selection])
                        print(user_selection_final)
                        break
                    elif response == 'r':
                        user_selection_final.extend([word for word,_ in user_selection])
                        self.see_related_choices(user_selection_final,adventure)
                        pass
                    elif response == 'q' or None:
                        return None
                    else: 
                        cprint("Invalid option try again..", color=PrintColors.system.value, on_color=PrintColors.error_on.value)
            
 
    def get_user_keyword_choices(self, 
                                 available_keyword_options: list):
        # take available keyword choices
        # convert into a table ready format 
        # display to user
        # take input
                # --> show contextual choices
        # ask if they want to make more input 
        # return the selected choices, adventure
        user_selection_final = list()
        while True:
            # ! Figure out how to handle when there are 0 related choices, the system breaks currently
            if len(available_keyword_options) == 0:
                cprint("\nNo related options available here...confirming selection so far!", color=PrintColors.error.value, on_color=PrintColors.error_on.value)
                return False, []
            print(tabulate(self.list_to_table_formatter(available_keyword_options)))
            user_index_selection = self.select_index_of_choices()
            
            if user_index_selection is None:
                return True, None
            
            user_selection = [(available_keyword_options[index]['keyword'], f">{available_keyword_options[index]['count']}<")
                              for index in user_index_selection]
            
            cprint("You selected the following: ", color = PrintColors.system.value)
            print(user_selection)
            cprint(self.option_string(purpose='index_selection'), color=PrintColors.system.value)
            response = input("--> ")
            while True:
                    if response == 'c':
                        user_selection_final.extend([word for word,_ in user_selection])
                        cprint("completed selection:", color=PrintColors.system.value)
                        print(user_selection_final)
                        return True, user_selection_final
                    elif response == 'a':
                        cprint("selection so far...", color=PrintColors.system.value)
                        user_selection_final.extend([word for word,_ in user_selection])
                        print(user_selection_final)
                        break
                    elif response == 'r':
                        user_selection_final.extend([word for word,_ in user_selection])
                        return False, user_selection_final
                        
                    elif response == 'q' or None:
                        return True, None
                    else: 
                        cprint("Invalid option try again..", color=PrintColors.system.value, on_color=PrintColors.error_on.value)
 
    
        
    def continue_orchestrator_input_choice(self):
        cprint("Ready to see matches? Press y if you are, any other key to keep adding.", color=PrintColors.system.value)
        user_choice = input("--> ")
        if user_choice.lower == 'y':
            return None

    
    def select_index_of_choices(self) -> list:
        while True:
            cprint("Enter selection as integer index. It will be added to selection", color=PrintColors.system.value)
            list_of_indexes = input("--> ")
            if list_of_indexes == 'q':
                return None
            try:
                list_of_indexes = list_of_indexes.split()
                list_of_indexes = [int(index) for index in list_of_indexes]
                return list_of_indexes
            except ValueError:
                cprint("You entered a non_integer value, try again..", color=PrintColors.system.value, on_color=PrintColors.error_on.value)
    
    
    def list_to_table_formatter(self, dict_list: list, row_size:int = 8):
        main_list = [(index, entry['keyword'],entry['count']) for index,entry in enumerate(dict_list)]
        broken_list = [main_list[i:i+row_size] for i in range(0,len(main_list),row_size)]
        return broken_list
    
    def option_string(self, purpose:str = None):
        if purpose is None: 
            return """v: (V)erb\tn: (N)oun\tpn: (P)roper (N)noun\t adj: (Adj)ective"""
        elif purpose == 'index_selection':
            return """\n (c)omplete selection, \t(r)elated choices, \t(a)dd options, \t(q)uit"""
        

    def selector_initializer(self):
        return { "order": set(),
                "selection": {
            "NOUN": [],
            "VERB": [],
            "ProperNoun": [],
            "ADJ": []
                }
        }