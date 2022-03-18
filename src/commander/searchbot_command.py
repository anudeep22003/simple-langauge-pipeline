#### Python Package Imports ####
from subprocess import call
import sys, os
from termcolor import cprint
from pprint import pprint
from tabulate import tabulate

#### Manual Import ####
from abstract_factory import Command, CommandHandler
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from neo4j_interfacer import Neo4jInterfacer



class SearchBotCommander(Command):
    
    """
    Purpose: Natural language search through your sidebrain graph
    
    Choose your adventure starting point:
    - Verb / Noun / Proper Noun / Adj / Domain 
    for every choice made, show related options that the user can add to their selection set
    - once done with a single choice, they can move on to another one (eg: first chose Verb --> listen, and)
    - at every choice they can confirm and finish and see all the returned 
    """
    
    def __init__(self, local_command_handler: CommandHandler, neointerface = Neo4jInterfacer) -> None:
        self.handler = local_command_handler()
        self.neo = neointerface()
        pass
    
    def orchestrate(self):
        while True:
            # cprint("yayy you're here in the bot, Imma kick you out now, but test passed.", color='red')
            user_adventure = self.handler.choose_your_adventure()
            if user_adventure is None:
                break
            elif not user_adventure:
                cprint("Let's try that again...", color='red', on_color='on_yellow')
                self.orchestrate()
            else:
                # do something with the chosen adventure
                cprint("What is the page size", color='red')
                user_selected_size = self.handler.size_chooser()
                cprint(f"chosen adventure is {user_adventure} and user selected size is {user_selected_size}", color = 'red')
                dict_list_of_keywords = self.show_contextual_adventure_choices(adventure = user_adventure, size=user_selected_size)
                # pprint(dict_list_of_keywords)
                tabular_ready_list = self.list_maker_to_tabulate(dict_list_of_keywords)
                # print(tabular_ready_list)
                print(tabulate(tabular_ready_list, tablefmt='grid'))
                
    
    
    def list_maker_to_tabulate(self, dict_list: list, row_size:int = 10):
        main_list = [(index, entry['keyword'],entry['count']) for index,entry in enumerate(dict_list)]
        broken_list = [main_list[i:i+row_size] for i in range(0,len(main_list),row_size)]
        return broken_list
    
    
    
    def show_contextual_adventure_choices(self, adventure: str, size: int):
        return self.query_runner(self.query_constructor(adventure, size))
    
    def query_constructor(self,adventure: str, size: int):
        return f"""match (k:Keyword:{adventure})-[r]-() 
    return k.word as keyword, count(r) as count 
    order by count desc
    limit {size}"""
    
    def query_runner(self, query):
        return self.neo.cypher_read_query_runner(query)
    
    pass