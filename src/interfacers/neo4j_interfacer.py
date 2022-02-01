from datetime import datetime
import json
from pickle import FALSE
from py2neo import Graph
from env_variables import EnvVariables
from pprint import pprint as pp
from neotime import DateTime

class Constructor:
    
    """
    Global Variable -> Py2Neo Graph object that establishes connection to to Neo4J DB
    
    Purpose:
    - The Constructor class does all the heavylifting of initializing a connection to the Neo4j DB.
    - It takes as an input a thread and converts that into a connected graph
    - It has helper functions to "construct" cypher queries for merge creating and connecting nodes.
    
    
    Functions

    - Init
        initializes self.errors to 0 to keep track of points of failures during execution.

    - thread_parser
        the main orchestrator of the constructor class. 
        (1) starts off by creating a parent node by accessing the top level key-value pairs
        (2) checks if thread has a 'children' key, if it does calls child_creator function 

    - parent_node_creator, meta_node_creator, child_node_creator
        constructs the actual cypher query using f-strings
    
    - cypher_runner
        (1) creates an auto-commiting transaction object that takes the query as an input and runs it
        (2) error handling: tries running the cypher query, if it fails prints error log to stdio and continues
            additionally also writes every query to a file and highlights the error separately to catch error points. 
    
    - cypher_logger (PENDING)
        purpose is to capture a log of every query transaction, yet to be built. 
    
    """
    
    
    GRAPH = Graph(EnvVariables.neo4j_creds['url'], auth = EnvVariables.neo4j_creds['auth'])
    #TXN = GRAPH.auto()

    def __init__(self) -> None:        
        """Create the py2neo transaction object here
        """
        #self.txn = Constructor.GRAPH.auto()
        self.errors = 0
        pass
    
    def thread_parser(self, thread: dict) -> None:        
        self.parent_node_creator(msg=thread)
        if 'children' in thread.keys():
            for child in thread['children']:
                self.child_node_creator(child)


    def parent_node_creator(self, msg: dict):
        q = f"""
        merge (:Parent :Message {{
        id: "{msg['id']}",
        type: "{msg['type']}",
        updated_at: datetime("{msg['updated_at']}"),
        idd: {msg['idd']},
        uri: {repr(msg['data']['uri'])}
        }})
        """

        self.cypher_runner(query=q)

        if msg['data']['link_title'] or msg['data']['link_img']:
            self.meta_node_creator(msg['data'], msg['id'])        



    def meta_node_creator(self, data: dict, id: str):
        q = f"""

        merge (m :Meta {{
        title: "{data['link_title']}",
        img: "{data['link_img']}",
        coords: "{data['coords']}"
        }})

        with m
        match (msg :Message)
        where msg.id = "{id}"
        merge (msg)-[:HAS_META]->(m)
        """

        self.cypher_runner(query=q)



    def child_node_creator(self, msg: dict):
        q = f"""
        merge (c :Child :Message {{
        id: "{msg['id']}",
        type: "{msg['type']}",
        parent_id: "{msg['parent_id']}",
        updated_at: datetime("{msg['updated_at']}"),
        idd: {msg['idd']},
        uri: {repr(msg['data']['uri'])}
        }})
        
        with c
        match (p :Parent)
        where p.id = c.parent_id
        merge (p)-[:HAS_CHILD]->(c)
        """
        self.cypher_runner(query=q)

        if msg['data']['link_title'] or msg['data']['link_img']:
            self.meta_node_creator(msg['data'], msg['id'])

    def cypher_runner(self, query):
        txn = Constructor.GRAPH.auto()
        try:
            txn.run(query)
        except:
            self.errors+=1
            print(f"error #{self.errors} skipped")
            query = '---'*5 + f' Error Point {self.errors} ' + '---'*5 + ' \n' + query 

        with open('src/knowledge_graph/sample_cypher_query.txt', mode='a') as f:
            f.write(query)
            f.write('\n\n')

    
class GraphExtractor:

    GRAPH = Graph(EnvVariables.neo4j_creds['url'], auth = EnvVariables.neo4j_creds['auth'])
    
    def __init__(self) -> None:
        pass
    
    def extract_orchestrator_debug(self, label_list:list=['Message','Meta']):
        for label in label_list:
            cypher = self.extract_query_generator(label)
            cursor_dict = self.extract_query_runner(cypher_query=cypher)
            if label == "Message":
                with open("glial-code/data_output/cypher_to_sql_message.txt", mode = 'a') as f:
                    for dict_entry in cursor_dict:
                        f.write(self.extract_message_property_extractor(cursor_dict_obj=dict_entry))
            if label == "Meta":
                with open("glial-code/data_output/cypher_to_sql_meta.txt", mode='a') as m:
                    for dict_entry in cursor_dict:
                        m.write(self.extract_meta_property_extractor(cursor_dict_obj=dict_entry))

        pass
    
    def extract_orchestrator_production(self, label):
        return self.extract_query_runner(self.extract_query_generator(label))

    
    def extract_query_generator(self, label = "Message"):
        if label == "Message":
            return "Match (m:Message) return m, labels(m) as labels, id(m) as id"
        else:
            return "Match (m:Meta) return m, labels(m) as labels, id(m) as id"

    def extract_query_runner(self, cypher_query:str):
        
        # returns a cursor object which is a Records object
        cursor_obj = GraphExtractor.GRAPH.run(cypher_query)
        # adding .data() converts to a dict object 
        return cursor_obj.data()
    
    # d is the neodatetime object
    def serialize_neo_datetime(self, d: DateTime):
        return datetime(d.year, d.month, d.day, d.hour, d.minute, int(d.second), tzinfo=d.tzinfo)
    
    def extract_message_property_extractor(self, cursor_dict_obj):
        
        # the node is a py2neo.Node.node object that needs to be converted into a dict to access
        node = dict(cursor_dict_obj['m'])
        
        try: 
            load_into_sql_list = [
                cursor_dict_obj['id'], 
                str(cursor_dict_obj['labels']),
                datetime.now(),
                datetime.now(),
                self.serialize_neo_datetime(node['updated_at']),
                node['uri']
                ]
        except:
            # load_into_sql_list = f"Error \n Node: {node}"
            print(f"Error \n Node: {node}")
            
        return load_into_sql_list
        
    def extract_meta_property_extractor(self, cursor_dict_obj):
        #img, title, 
        # the node is a py2neo.Node.node object that needs to be converted into a dict to access
        node = dict(cursor_dict_obj['m'])
        
        try: 
            load_into_sql_list = [
                cursor_dict_obj['id'], 
                str(cursor_dict_obj['labels']),
                datetime.now(),
                datetime.now(),
                node['title'],
                node['img']
                ]
        except:
            # load_into_sql_list = f"Error \n Node: {node}"
            print(f"Error \n Node: {node}")
            
        return load_into_sql_list
        

    def cypher_logger():
        pass

    def sample_query(self):
        txn = Constructor.GRAPH.auto()
        cypher_query = "Match (p:Parent) return p, labels(p) as labels, id(p) as id"
        cursor_obj = txn.run(cypher=cypher_query)
        cursor_dict_obj = cursor_obj.data()
        print(type(cursor_obj))
        
        i = 0
        print("first print of ** Cursor_Dict_Obj **", end = '\n')
        for item in cursor_dict_obj:
            print(f"The type of each item is: {type(item)}")
            print("Item print\n")
            pp(item)
            print('\n')
            print("labels and their type\n")
            print(f" label: {item['labels']}\n Type: {type(item['labels'])}\n")
            print(" Node and their type\n")
            print(f" Node: {item['p']}\n Type: {type(item['p'])}\n")
            
            i+=1

            if i == 2:
                break
            else: continue
                
            
    
if __name__ == "__main__":
    g = GraphExtractor()
    g.extract_orchestrator_debug()
    pass
