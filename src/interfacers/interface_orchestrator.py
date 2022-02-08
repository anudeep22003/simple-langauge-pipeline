from cProfile import label
from neo4j_interfacer import GraphExtractor
from sqlite_interfacer import SqlInitializer, SqlInterfacer
from sb_backend_interfacer import ApiDataExtractor


"""
- ETL Process:
    - Download data from SB backend via API
    - Construct a graph in Neo4J using the downloaded data
- Handle api pagination and repeat ETL process above till end of data
"""
## commenting this out since its already done
## uncomment when you want this process to run afresh
# a = ApiDataExtractor()


"""
- Extract data from Graph 
- construct index in SQLite
"""

class GraphToSqlLoader:
    
    def __init__(self, labels: list) -> None:
        self.graph_interface = GraphExtractor()
        self.sqlite_interface = SqlInitializer()
        self.labels = labels
        pass
    
    def orchestrator(self):
        for label in self.labels:
            for dict_item in self.graph_interface.extract_orchestrator_production(label):
                self.graph_extract_sql_loader(dict_record=dict_item, label=label)
            
        pass
    
    def graph_extract_sql_loader(self, dict_record: dict, label: str):
        
        if label == "Message":
            data = self.graph_interface.extract_message_property_extractor(dict_record)
        elif label == "Meta":
            data = self.graph_interface.extract_meta_property_extractor(dict_record)
        else:
            print("Unexpected label type")

        query = self.sqlite_interface.insert_query_generator(label)
        SqlInterfacer.INSERT_QUERY_RUNNER(query, data)
        
        pass
    
    pass


label_list = ["Message", "Meta"]

g = GraphToSqlLoader(labels=label_list)
g.orchestrator()
