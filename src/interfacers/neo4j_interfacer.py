from datetime import datetime, tzinfo, timezone
import json
from pickle import FALSE
from typing import Dict
from py2neo import Graph
from env_variables import EnvVariables
from pprint import pprint as pp
from neotime import DateTime

import os, sys
sys.path.append(os.path.join(os.getcwd(),'src','glial_code'))
from decorators import Decorators

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
        self.neo_interfacer = Neo4jInterfacer()
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

        self.neo_interfacer.cypher_write_query_runner(query=q)

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

        self.neo_interfacer.cypher_write_query_runner(query=q)



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
        self.neo_interfacer.cypher_write_query_runner(query=q)

        if msg['data']['link_title'] or msg['data']['link_img']:
            self.meta_node_creator(msg['data'], msg['id'])

    def cypher_runner(self, query):
        txn = self.neo_interfacer.graph.auto()
        try:
            txn.run(query)
        except:
            self.errors+=1
            print(f"error #{self.errors} skipped")
            query = '---'*5 + f' Error Point {self.errors} ' + '---'*5 + ' \n' + query 

        with open('/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/sample_cypher_query.txt', mode='a') as f:
            f.write(query)
            f.write('\n\n')

    
class GraphExtractor:
    
    """
    
    Purpose:
    A class to help with ETL of data from graph db to other databases. 
    To `extract` data from the graph db and `transform` it into a sequence of list objects that can be used to `load` into other databases (tested for sqllite)
    
    ******* Functions: ********
    
    - extract_orchestrator_debug (default switched off, switched on to debug)
    Orchestrates the entire extraction calling all the necessary class functions to sybchronize a total extract of the data in the Neo4j db
    (1) takes as an input the least common denominator of unique labels in the graph db
    (2) writes the list output of each dict item in the cursor to a file for inspection of errors 
    
    - extract_orchestrator_production
    Takes a label as an input -> generates respective query to extract data -> runs the query \
    -> returns data as a dict
    
    - extract_query_generator
    Generates a query to return all the nodes of that label type from the graph db based on the passed label     
    
    - extract_message_property_extractor
    Convert the (message) node object that is in the dict returned by the cursor, and serializes the data into an ordered list that can be loaded into a sql db. 
    
    - extract_meta_property_extractor
    Convert the (meta) node object that is in the dict returned by the cursor, and serializes the data into an ordered list that can be loaded into a sql db. 

    - sample_query
    Not part of the main class, created to test the methods of the class when debugging

    """

    GRAPH = Graph(EnvVariables.neo4j_creds['url'], auth = EnvVariables.neo4j_creds['auth'])
    
    def __init__(self) -> None:
        self.neo_interfacer = Neo4jInterfacer()
        pass
    
    def extract_orchestrator_debug(self, label_list:list=['Message','Meta']):
        for label in label_list:
            cypher = self.extract_query_generator(label)
            cursor_dict = self.neo_interfacer.cypher_read_query_runner(cypher_query=cypher)
            if label == "Message":
                with open("glial-code/data_output/cypher_to_sql_message.txt", mode = 'a') as f:
                    for dict_entry in cursor_dict:
                        f.write(self.extract_message_property_extractor(cursor_dict_obj=dict_entry))
            if label == "Meta":
                with open("glial-code/data_output/cypher_to_sql_meta.txt", mode='a') as m:
                    for dict_entry in cursor_dict:
                        m.write(self.extract_meta_property_extractor(cursor_dict_obj=dict_entry))

        pass
    
    def extract_orchestrator_production(self, label) -> dict:
        return self.neo_interfacer.cypher_read_query_runner(self.extract_query_generator(label))

    
    def extract_query_generator(self, label = "Message") -> str:
        if label == "Message":
            return "Match (m:Message) return m, labels(m) as labels, id(m) as id"
        else:
            return "Match (m:Meta) return m, labels(m) as labels, id(m) as id"
 
    
    def extract_message_property_extractor(self, cursor_dict_obj) -> list:
        
        # the node is a py2neo.Node.node object that needs to be converted into a dict to access
        node = dict(cursor_dict_obj['m'])
        
        try: 
            load_into_sql_list = [
                cursor_dict_obj['id'], 
                str(cursor_dict_obj['labels']),
                datetime.now(tz=timezone.utc),
                datetime.now(tz=timezone.utc),
                self.neo_interfacer.serialize_neo_datetime(node['updated_at']),
                node['uri']
                ]
        except:
            # load_into_sql_list = f"Error \n Node: {node}"
            load_into_sql_list = ["","","","","",""]
            print(f"Error \n Node: {node}")
            
        return load_into_sql_list
        
    def extract_meta_property_extractor(self, cursor_dict_obj) -> list:
        #img, title, 
        # the node is a py2neo.Node.node object that needs to be converted into a dict to access
        node = dict(cursor_dict_obj['m'])
        
        try: 
            load_into_sql_list = [
                cursor_dict_obj['id'], 
                str(cursor_dict_obj['labels']),
                datetime.now(tz=timezone.utc),
                datetime.now(tz=timezone.utc),
                node['title'],
                node['img']
                ]
        except:
            # load_into_sql_list = f"Error \n Node: {node}"
            load_into_sql_list = ["","","","","",""]
            print(f"Error \n Node: {node}")
            
        return load_into_sql_list


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
                
            
@Decorators.singleton
class Neo4jInterfacer:
    
    """
    
    Purpose:
    A singleton class to help to interface with Neo4j
    
    Attributes:
    graph object --> initializes a connection to the graph database

    ******* Functions: ********
    
    - cypher_read_query_runner
        Takes a well constructed query as an input and interaces with the GRAPH object to run the query and return the output. 
        The output is returned in a dict form (for each row)
        
    - cypher_write_query_runner
        Takes a fully constructer write query (data included) and runs it. No return type.
    
    - serialize_neo_datetime
        Neo4j uses its own proprietary datetime format for storing dates
        this method deserializes that into a python datetime object 
        
    - serialize_py_datetime
        This method serializes a python datetime object into a Neo4j DateTime object
    
    
    """
    
    
    def __init__(self) -> None:
        self.graph = Graph(EnvVariables.neo4j_creds['url'], auth = EnvVariables.neo4j_creds['auth'])
        self.errors = 0
        pass
    
    def cypher_read_query_runner(self, cypher_query:str) -> dict:
        
        # returns a cursor object which is a Records object
        cursor_obj = self.graph.run(cypher_query)
        # adding .data() converts to a dict object 
        return cursor_obj.data()
    
    
    def cypher_write_query_runner(self, query):
        txn = self.graph.auto()
        try:
            txn.run(query)
        except Exception as e:
            self.errors+=1
            print(f"error #{self.errors} skipped, exception: {type(e)}, args: {e.args}")
 
    
    def serialize_neo_datetime(self, d: DateTime) -> datetime:
        return datetime(d.year, d.month, d.day, d.hour, d.minute, int(d.second), tzinfo=d.tzinfo)
    
    def serialize_py_datetime(self,d:datetime):
        return DateTime(d.year, d.month, d.day, d.hour, d.minute, d.second, tzinfo=d.tzname())

    
    pass






if __name__ == "__main__":
    #g = GraphExtractor()
    # g.extract_orchestrator_debug()
    pass
