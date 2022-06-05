#### Python Package Imports ####
import sys, os
from termcolor import colored, cprint
from collections import defaultdict

#### Manual Import ####
from abstract_factory import Command, CommandHandler
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from neo4j_interfacer import Neo4jInterfacer
from enum_factory import PrintColors

class TagCommand(Command):
    
    def orchestrate(self):
        self.take_user_input()
        pass
    
    def take_user_input(self):
        print("You are in the tagging experience!")
        while True:
            print("Do you want to continue?")
            user_input = input('--> ')
            if user_input == 'e':
                print("exiting")
                break

class QuitCommand(Command):
    
    def orchestrate(self):
        print("Exiting now....")
        sys.exit()

class KeywordCleanerCommand(Command):
    
    def __init__(self, local_command_handler: CommandHandler, neointerface = Neo4jInterfacer) -> None:
        self.neo = neointerface()
        self.selection_set = list()
        self.handler = local_command_handler()
        self.adventure_history = list()
        
        self.parse_complete_dict = defaultdict(list)
        self.current_parse_accepted_dict = defaultdict(list)
        self.delete_complete_dict = defaultdict(list)
        pass
    
    def orchestrate(self):
        while True:
            user_adventure_choice = self.handler.initialize_game()
            if not user_adventure_choice:
                self.orchestrate()
            elif user_adventure_choice == 'quit':
                break
            else:
                self.adventure_history.append(user_adventure_choice)
                current_adventure = self.adventure_history[-1]
                
                # using default dict and making sure that entries for each adventure type are initialized
                self.create_dict_entries(current_adventure)
                
                list_to_process = self.start_subgame(current_adventure)
                if list_to_process is None:
                    break
                else:
                    self.user_input_iterator(list_to_process, current_adventure)
                    
    def create_dict_entries(self, adventure: str):
        self.parse_complete_dict[adventure]
        self.current_parse_accepted_dict[adventure]
        self.delete_complete_dict[adventure]
    
    
    
    def option_string(self):
        return """Your options are: \t ↵ (keep)\t r: (r)emove\tce: (c)omplete & (e)xit \taq: (a)bort and (q)uit"""
    
    
    def start_subgame(self, user_adventure):
        cprint("--> How many do you want to get through today\t",color=PrintColors.system.value)
        print("exit by pressing q: to (q)uit")
        
        user_input = input("Enter your choice\t--> ")
        
        if user_input == 'q':
            return None
        else: 
            input_size = int(user_input)    
            continue_index = len(self.parse_complete_dict[user_adventure]) - len(self.delete_complete_dict[user_adventure])
            last_index = int(input_size) + continue_index
            cprint(f"Ok, we will start from #{continue_index} and go till #{last_index}", color=PrintColors.system.value)
            cprint(self.option_string(),color='yellow', on_color='on_grey')
        
            # each item of the list is a dict with keys: `word` and `count`
            
            return self.list_nodes(last_index,adventure=user_adventure)[continue_index:last_index]     

            
    
    def delete_selection(self, current_adventure):
        
        if len(self.selection_set) == 0:
            self.cleanup_selection(current_adventure)
        else:
            cprint(f"You are about to delete the following nodes: \n>>type: [{current_adventure}] \t >> [{self.selection_set}]\t")

            user_confirmation = input("> Press y to continue with deletion, or ANY other key to exit ")
            if user_confirmation.lower() == 'y':
                q = f"""MATCH (k:Keyword:{current_adventure}) 
                WHERE k.word IN {self.selection_set}
                DETACH DELETE k
                """        
                self.neo.cypher_write_query_runner(q)
                print(f"removed following words and added to log: \n>> [{self.selection_set}]")
                self.delete_complete_dict[current_adventure].extend(self.selection_set)
                self.cleanup_selection(current_adventure)
            else: 
                self.abort_without_delete(current_adventure)
            
    
    def cleanup_selection(self, adventure):
        cprint(("selection list",self.selection_set), color = PrintColors.feedback.value)
        self.selection_set.clear()
        self.parse_complete_dict[adventure].extend(self.current_parse_accepted_dict[adventure])
        cprint((f"parse complete list for {adventure}",self.parse_complete_dict[adventure]), color = PrintColors.feedback.value)
        cprint((f"parse accepted list for {adventure}",self.current_parse_accepted_dict[adventure]), color = PrintColors.feedback.value)
        self.current_parse_accepted_dict[adventure].clear()
        cprint("Cleaned up the current selection for the next round....", color = PrintColors.feedback.value)
        
    def add_to_selection(self, word):
        self.selection_set.append(word)
    
    def abort_without_delete(self, current_adventure: str):
        print("Aborting without deleting anything...")
        self.cleanup_selection(current_adventure)
        print("Taking you to the start of the subgame.....")
        self.orchestrate()

    def user_input_iterator(self, entries: list, current_adventure: str):
        while True:
            for entry in entries:
                print(f"({entry['word']}, #{entry['count']})", end='\t')
                user_input = input("---> ")
                
                if user_input == "":
                    self.current_parse_accepted_dict[current_adventure].append(entry['word'])
                    pass
                
                elif user_input == 'r':
                    # add to the selector
                    self.add_to_selection(entry['word'])
    
                elif user_input == 'ce':
                    # complete the deletion of selection 
                    pass
                
                elif user_input == 'aq':
                    self.abort_without_delete(current_adventure)
                
                else:
                    print("Invalid option selected. Your options are:\n")
                    print(self.option_string())
                
            self.delete_selection(current_adventure)
            break
    
    
    
    def list_nodes(self, size: int, adventure: str):
        # list nodes by their count
        # contruct a query
        # run query
        # display data to user 
        
        return self.query_runner(self.query_constructor(size, adventure))
        
    
    def query_constructor(self, size: int, adventure:str):
        return f"""Match (k:Keyword:{adventure})-[r]-(m)
        Return k.word as word, count(r) as count
        Order by count DESC LIMIT {int(size)}
        """
    
    def query_runner(self, cypher_query):
        return self.neo.cypher_read_query_runner(cypher_query)    