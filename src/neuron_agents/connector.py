

import os, sys
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from neo4j_interfacer import Neo4jInterfacer

class Connector:
    """
    Purpose: A generalized agent that can merge relationships and relationship properties
    
    Approach:
    
    Input required: 
    - Nodes --> two nodes to make the connection between #! (v2 --> generalize to multi nodes)
        - make this a tuple
        - what informtion about the node do you pass? --> id?
    - Relationship --> the relationship {name} and properties: {property_name: property_value}
        - make this a dict list: [{name}, {properties}]
        - not one because sometimes the property name could be `name.` We dont want the system to break when this happens
    
    Process: 
    - identify the nodes using a match clause, and remember the identity
    - f-string the relationship name and properties into a cypher clause and run it
    
    Functions:
    init 
    - neo4j interfacer --> run read/write cypher clauses
    
    orchestrator:
    - accepts as argument - ((node-A, node-B), rel_data)
    
    node_verifier
    - verifies the existence of the two nodes through a read match clause
    - True if exists, and false if fails 
    
    r_data_template
    - return a shaped dict, as {starting node, ending node, relationship_name, relationship_direction, relationship_properties}
    - a function will use this as the template to ask for a connection to be made
    
    r_property_query_initializer
    - iterates over the dict of properties and constructs the property query to be added into the main merge query
    
    r_connector
    - constructs the connect cypher clause and runs it.
    
    
    
    node_property_updater
    - if adding a connection involves setting a property of the node
    
    
    Misc notes:
    - This agent cannot create nodes, only connect nodes that have been passed to it
    
    """    
    
    def __init__(self) -> None:
        self.neo = Neo4jInterfacer()
        self.merge_count = 0
        pass
    
    def orchestrator(self, r_data):
        # verify the existence of the nodes
        if self.node_verifier(r_data["start_node"],r_data["end_node"]):
            self.r_connector(r_data)
    
    def node_verifier(self,start_id,end_id):
        #match clause construction
        q = f"""
            MATCH (n)
            where id(n) in [{start_id},{end_id}]
            return n
        """
        
        try:
            self.neo.cypher_read_query_runner(q)
        except Exception as e:
            print(f"Node not found\nException: {type(e)}")
            return False
        else:
            return True
        
    def r_property_query_initializer(self,r_property: dict):
        q = ""
        for k,v in r_property.items():
            q+=f"{k}: {repr(v)}, "
        return q[:-2]
    
    def r_data_template(self):
        
        return {
            "start_node": "",
            "end_node": "",
            "r_name":"",
            "r_direction_towards":"end",
            "r_properties":{}
        }        
    
    def r_connector(self,r_data: dict):
        q = f"""
            match (s)
            where id(s)={r_data['start_node']}
            match (e)
            where id(e)={r_data['end_node']}
            merge (s)-[r:{r_data["r_name"]} 
                {{ 
                
                {self.r_property_query_initializer(r_data['r_properties'])}
                
                }}
                ]->(e)
            
        """
        
        self.neo.cypher_write_query_runner(q)
        print(f"Merge #{self.merge_count} completed.")
        self.merge_count+=1


if __name__ == "__main__":
    c = Connector()
    # c.orchestrator()