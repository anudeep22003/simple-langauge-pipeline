import sys, os
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))

from neo4j_interfacer import Neo4jInterfacer
from pprint import pprint as pp


class Placeholder:
    
    def __init__(self, neointerface: Neo4jInterfacer) -> None:
        self.neo = neointerface()
        self.selection = set()
        self.size_start = 0
        pass
    
    def query_constructor(self, size):
        return f"""Match (k:Keyword:VERB)-[r]-(m)
        Return k.word as word, count(r) as count
        Order by count DESC LIMIT {int(size)}
        """

    
    def query_runner(self, cypher_query):
        return self.neo.cypher_read_query_runner(cypher_query)
        
    
    def list_nodes(self, size):
        # list nodes by their count
        return self.query_runner(self.query_constructor(size))
        # contruct a query
        # run query
        # display data to user 
        
        pass
    
    def selector(self, item):
        # add to selection
        self.selection.add(item)
        pass
    
    def executor(self,size):
        # remove the nodes
        list_of_nodes = list(self.selection)
        q = f"""Match (k:Keyword:VERB) 
        where k.word in {list_of_nodes}
        detach delete k
        """
        self.neo.cypher_write_query_runner(q)
        print(f"removed following words: \n {list_of_nodes}")
        self.size_start = self.size_start + (len(self.selection)- size)
        self.selection = set()
        print("Emptied selection for next round")
        pass
    
    def user_interfacer(self):
        """
        Steps:
        - ask user for session size 
        - show one by one (also progress, #left)
            - for each, take input from user - {keep, remove, complete_selection, abort_process}
        """
        
        input_size = input("How many do you want to get through today\t")
        last_index = int(input_size) + self.size_start
        print(f"Ok, we will start from #{self.size_start} and go till #{last_index}")
        print("Your options are: \n ↵ (keep)\n r (remove)\n e (exit but complete) a (abort entirely)")
        d = self.list_nodes(last_index)
        

        for i in range(len(d))[self.size_start:]:
            r = self.user_input_iterator(d[i])
            if r == -1:
                break
            elif r:
                pass
            else:
                self.executor(int(input_size))
                break
        
    
    def user_input_iterator(self, entry):

        print(f"({entry['word']}, #{entry['count']})", end='\t')
        user_input = input("---> ")
        return self.action_selector(user_input, entry['word'])
        
    
    def action_selector(self, input:str = 'start', word: str = None):
        if input == "":
            return 1
        elif input == 'r':
            self.selector(word)
            return 1
        elif input == 'e':
            return 0
        elif input == 'start' and word is None:
            print("starting the loop")
            return 1
        elif input == 'a':
            print("Aborting without executing")
            return -1
        else:
            print('Invalid option exiting')
            return 0
        
            
    
    pass


if __name__ == "__main__":
    
    p = Placeholder(Neo4jInterfacer)
    p.user_interfacer()
    pass