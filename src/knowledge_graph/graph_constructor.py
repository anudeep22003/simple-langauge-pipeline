import json
from py2neo import Graph

    """[summary]
    """class Constructor:    
    
    
    GRAPH = Graph("neo4j+s://8219a15b.databases.neo4j.io:7687", auth = ("neo4j", "SHHcaUZYNPF-qWoyOrahHksjOelYBFASgdqjrRd1Ju8"))
    #TXN = GRAPH.auto()

    def __init__(self) -> None:
        """Create the py2neo transaction object here
        """
        self.txn = Constructor.GRAPH.auto()
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


