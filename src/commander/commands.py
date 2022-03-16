from abstract_factory import Command
import sys, os
from termcolor import colored, cprint
#### Manual Import ####
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from neo4j_interfacer import Neo4jInterfacer


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
    
    def __init__(self, neointerface = Neo4jInterfacer) -> None:
        self.neo = neointerface()
        self.selection_set = set()
        self.parse_complete = list()
        self.current_parse_accepted_list = list()
        self.delete_complete = list()
        pass
    
    def orchestrate(self):
        while True:
            d = self.start_subgame()
            if d == 'quit':
                break
            else:
                self.user_input_iterator(d)
                
            
    
    
    
    
    def option_string(self):
        return """Your options are: \t ↵ (keep)\t r: (r)emove
\tce: (c)omplete & (e)xit \taq: (a)bort and (q)uit"""
    
    def start_subgame(self):
        cprint("--> How many do you want to get through today\t",color='red')
        print("exit by pressing q: to (q)uit")
        
        user_input = input("Enter your choice\t--> ")
        
        if user_input == 'q':
            return 'quit'
        else: 
            input_size = int(user_input)
            continue_index = len(self.parse_complete) - len(self.delete_complete)
            last_index = int(input_size) + continue_index
            cprint(f"Ok, we will start from #{continue_index} and go till #{last_index}", color='red')
            cprint(self.option_string(),color='yellow', on_color='on_grey')
        
            # each item of the list is a dict with keys: `word` and `count`
            
            return self.list_nodes(input_size)[continue_index:last_index]            

            
    
    def delete_selection(self):
        list_of_nodes_to_remove = list(self.selection_set)
        print(f"You are about to delete the following nodes: \n>> [{list_of_nodes_to_remove}]")
        user_confirmation = input("> Press y to continue with deletion, or ANY other key to exit ")
        if user_confirmation.lower() == 'y':
            q = f"""MATCH (k:Keyword:VERB) 
            WHERE k.word IN {list_of_nodes_to_remove}
            DETACH DELETE k
            """        
            self.neo.cypher_write_query_runner(q)
            print(f"removed following words and added to log: \n>> [{list_of_nodes_to_remove}]")
            self.delete_complete.extend(list_of_nodes_to_remove)
            self.cleanup_selection()
        else: 
            self.abort_without_delete()
            
    
    def cleanup_selection(self):
        print(("selection list",self.selection_set), sep = '\t')
        self.selection_set.clear()
        self.parse_complete.extend(self.current_parse_accepted_list)
        print(("parse complete list",self.parse_complete), sep = '\t')
        print(("parse accepted list",self.current_parse_accepted_list), sep = '\t')
        self.current_parse_accepted_list.clear()
        print("Cleaned up the current selection for the next round....")
        
    def add_to_selection(self, word):
        self.selection_set.add(word)
    
    def abort_without_delete(self):
        print("Aborting without deleting anything...")
        self.cleanup_selection()
        print("Taking you to the start of the subgame.....")
        self.orchestrate()

    def user_input_iterator(self, entries):
        while True:
            for entry in entries:
                print(f"({entry['word']}, #{entry['count']})", end='\t')
                user_input = input("---> ")
                
                if user_input == "":
                    self.current_parse_accepted_list.append(entry['word'])
                    pass
                
                elif user_input == 'r':
                    # add to the selector
                    self.add_to_selection(entry['word'])
    
                elif user_input == 'ce':
                    # complete the deletion of selection 
                    pass
                
                elif user_input == 'aq':
                    self.abort_without_delete()
                
                else:
                    print("Invalid option selected. Your options are:\n")
                    print(self.option_string())
                
            self.cleanup_selection()
            break
    
    
    
    def list_nodes(self, size):
        # list nodes by their count
        # contruct a query
        # run query
        # display data to user 
        
        return self.query_runner(self.query_constructor(size))
        
    
    def query_constructor(self, size):
        return f"""Match (k:Keyword:VERB)-[r]-(m)
        Return k.word as word, count(r) as count
        Order by count DESC LIMIT {int(size)}
        """
    
    def query_runner(self, cypher_query):
        return self.neo.cypher_read_query_runner(cypher_query)    