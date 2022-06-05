#### Python Package Imports ####
from subprocess import call
import sys, os
from pprint import pprint
from numpy import full
from pyparsing import col
from termcolor import cprint

#### Manual Import ####
from abstract_factory import Command, CommandHandler
from enum_factory import PrintColors, AdventureOptions
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
        self.current_output_list_of_keywords = None
        self.number_of_active_selectors = 0
        self.current_active_selector = self.selector_initializer()
        self.matchcommander = MatchCommander()
        pass
    
    def orchestrate(self):
        while True:
            size, adventure = self.handler.user_input_orchestrator()
            
            if size is None or adventure is None:
                break
            else:
                user_selection = self.keyword_choice_orchestrator(adventure,size)
                if user_selection is None:
                    break

                cprint("\nSelector state:\n", color=PrintColors.feedback.value)

                # add to selector
                self.add_choice_to_selector_dict(adventure, user_selection)
                cprint(self.current_active_selector, color=PrintColors.test.value)
                
                # if two adventures are complete show match option 
                if len(self.current_active_selector['order']) == 2:
                    break
                
                # # allow user to complete selection and get matches
                # if self.handler.continue_orchestrator_input_choice() is None:
                #     break
                # else:
                #     continue
        
        self.matchcommander.orchestrate(self.current_active_selector)
                
                
    def keyword_choice_orchestrator(self, adventure: AdventureOptions, size: int = 40, context: list = None):
        available_keyword_options = self.show_keyword_choices(adventure, size, selected_context=context)
        user_selection = self.get_user_keyword_selection(available_keyword_options, adventure)
        if user_selection is None:
            return None
        else:
            cprint("\nYour selection is:", color=PrintColors.feedback.value)
            cprint(user_selection, color = PrintColors.feedback.value)
            
            return user_selection           
    
    
    def add_choice_to_selector_dict(self, adventure: AdventureOptions, user_selected_keywords: list):
        
        selector = self.selector_initializer()
        selector['order'].append(adventure.name)
        selector['selection'][adventure.name].extend(user_selected_keywords) 
        
        return selector
        
    
                
    def get_user_keyword_selection(self, 
                                   available_keyword_options: list,
                                   adventure_choice:AdventureOptions):
        
        """
        Take the keyword choices, and get user's selection 
        """
        full_full_selection = []
        
        complete_flag, user_selection = self.handler.get_user_keyword_choices(available_keyword_options)
        
        if user_selection is None:
            return None
        
        full_full_selection.extend(user_selection)
        
        if not complete_flag and len(user_selection) != 0:       
                
            newly_available_keyword_options = self.show_keyword_choices(adventure=adventure_choice, selected_context=user_selection)
            related_user_selection = self.get_user_keyword_selection(newly_available_keyword_options, adventure_choice)
            if related_user_selection is None:
                return None
        
            full_full_selection.extend(related_user_selection)
        
        return full_full_selection
            
            
        
    
    
    def show_keyword_choices(self, adventure: AdventureOptions, size: int=30, selected_context: list = None):
        return self.query_runner(self.query_constructor(adventure, size, selected_context))
    
    def query_runner(self, query):
        with open("src/commander/cypher_queries.txt", mode='a') as f:
            f.write(f"\n{query}\n")
        return self.neo.cypher_read_query_runner(query)
    
    
    def query_constructor(self,adventure: AdventureOptions, size: int, selected_context: list = None):
        if selected_context is None:
            return f"""match (k:Keyword:{adventure.name})-[r]-() 
        return k.word as keyword, count(r) as count 
        order by count desc
        limit {size}"""
        else:
            return f"""match (k:Keyword:{adventure.name})--()-[r]-(tk:Keyword:{adventure.name})
        where k.word in {selected_context}
        return k.word as context_keyword, tk.word as keyword, count(r) as count
        order by count desc
        limit {size}"""
    
    
    def selector_initializer(self):
        if self.number_of_active_selectors > 0:
            return self.current_active_selector
        else:
            self.number_of_active_selectors+=1
            return { "order": list(),
                    "selection": {
                "NOUN": [],
                "VERB": [],
                "ProperNoun": [],
                "ADJ": []
                    }
            }
            
            
class MatchCommander(Command):
    
    """
    This command class is responsible for orchestrating and interacting with matches.
    It will accept a list of keywords in a dict form, in the order that they come through 
    It will first show a level 1 match i.e. all items that are directly connected to the chosen tags 
    """
    
    def __init__(self, neointerface = Neo4jInterfacer, local_command_handler: CommandHandler = None) -> None:
        self.selection = None
        self.neo = neointerface()
        pass
    
    def orchestrate(self, selector: dict):
        cprint("Entered into the match commander...", color=PrintColors.system.value)
        self.selection = selector
        pprint(self.show_matches())
        pass
    
    def show_matches(self):
        
        order_of_processing = self.selection['order']
        selection = self.selection['selection']
        
        if len(order_of_processing)>2:
            return "currently only supprt depth of two"
        
        k = selection[order_of_processing[0]]
        tk = selection[order_of_processing[1]]
        
        dict_data_response = self.query_runner(self.query_contructor(k, tk))
        return self.parse_matches(dict_data_response)

    def parse_matches(self, dict_data: list):
        response_list  = list()
        for item in dict_data:
            target_node = item['m']
            key = dict(item['keys'])
            dict_node = dict(target_node)
            try:
                response_list.append((f"key: {key['word']}      #hops={item['l']}" ,str(dict_node['uri'])))
            except KeyError:
                response_list.append((f"key: {key['word']}      #hops={item['l']}" ,str(dict_node['title'])))
        return response_list
    
    
    def query_runner(self, query):
        with open("src/commander/cypher_queries.txt", mode='a') as f:
            f.write(f"\n{query}\n")
        return self.neo.cypher_read_query_runner(query)
    
    def query_contructor(self, keyword: list, target_keyword: list):
        
        if target_keyword is None:
                q = f"""
        match p=(k:Keyword)--(m)
        where k.word in {keyword} and (m:Message or m:Meta)
        return distinct(k) as keys, m, length(p) as l
        order by l desc
        """

        else:
            
            q = f"""
            match p=(k:Keyword)--(m)-[*0..2]-(tk:Keyword)
            where k.word in {keyword} and tk.word in {target_keyword} and (m:Message or m:Meta)
            return distinct(k) as keys, m, length(p) as l
            order by l desc
            """
        return q
    
    pass