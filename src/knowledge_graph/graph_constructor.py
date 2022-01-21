import json
from py2neo import Graph
from env_variables import EnvVariables
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


    def cypher_logger():
        pass


