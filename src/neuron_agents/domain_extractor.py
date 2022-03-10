from datetime import datetime, timezone
import re, sys
from time import time
from tld import get_tld
import os
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))

from sqlite_interfacer import SqlInterfacer
from neo4j_interfacer import GraphExtractor, Neo4jInterfacer


class DomainExtractorAgent:
    
    """
    Steps:
    - generate a sql query to extract the relevant column
    - run the sql query and receive the row_list
    - for every row returned, run it through a regex matcher and extract the url from it
        - id, uri
    - run the url through a third party domain-extractor and store the sub-domain and domain
    
    Initialization:
    - add a new column to sql table 'domain extracted date' 
    
    Next:
    - Cypher:
        - match on the id of the node being processed
        - merge a domain node and a relationship into the graph [:DOMAIN_OF]
        - if succesful add a domain_extracted property and initializse with current date
    - add datetime.now to sql column 'domain extracted date'
    """
    def __init__(self) -> None:
        self.url_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')
        self.neo_worker = Neo4jInterfacer()
        self.sql_worker = SqlInterfacer()
        self.run = 0
        pass
    
    def sql_query_generator(self):
        return "Select node_id, uri from message_index"
    
    def sql_query_executor(self, query:str):
        # print([r for r in  self.sql_worker.read_query_runner(query)])
        return self.sql_worker.read_query_runner(query)
    
    def orchestrator(self):
         for row in self.sql_query_executor(self.sql_query_generator()):
             id = row[0]
             for match in self.url_extractor(row[1]):
                domain_dict = self.url_parser(url=match[0])
                self.add_query_runs(id,domain=domain_dict['domain'])
                print(f"ROW {self.run} COMPLETE")
                self.run+=1
                
    
    def url_extractor(self, string_to_process:str):
        return re.findall(self.url_pattern, string_to_process)
    
    def domain_disambiguator(self,s):
        s = str(s).title()
        if s == 'Youtu':
            return 'Youtube'
        else: 
            return s
    
    def url_parser(self,url):
        
        try:
            res = get_tld(url, as_object=True,fail_silently=True)
            # self.writer("res: {:<15s}\tsubdomain: {:<10s}\tdomain: {:<20s}\ttld: {:<10s}\tfld: {:<25s}\turl: {:<s}\n".format(str(res), str(res.subdomain), str(res.domain), str(res.tld), str(res.fld), url))
        
            return {
                'res':str(res),
                'subdomain': str(res.subdomain),
                'domain': self.domain_disambiguator(res.domain),
                'tld': str(res.tld)
            }
        except Exception as e:
            
            print(f"Exception skipped: {type(e)!r}\t args: {e.args}")
            
            return {
                'res':"",
                'subdomain': "",
                'domain': f"Exception caught: {type(e)!r}\t args: {e.args}",
                'tld': ""
            }
        
    
    def writer(self, content):
        with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/extracted_urls.txt", mode='a') as f:
            f.write(content)
        pass
    
    def add_query_runs(self, id, domain):

        q_neo_merge = f"""
            MATCH (m) 
            WHERE id(m)= {id}
            WITH m
            MERGE (d:Domain {{domain: "{domain}"}})
            MERGE (d)-[r:DOMAIN_OF]->(m)    
            """
        #run the query
        self.neo_worker.cypher_write_query_runner(q_neo_merge)
        print("merge success.", end='\t')
        
        d = datetime.now(tz=timezone.utc)
            
        q_neo_add_property = f"""
            MATCH (m)
            WHERE id(m)={id}
            WITH m
            SET m.domain_extracted_date = datetime('{d.isoformat()}')
            """
        
        # run the query 
        self.neo_worker.cypher_write_query_runner(q_neo_add_property)
        print("property add success.", end='\t')

        q_sql_add_log = """
            UPDATE message_index
            SET (domain_extracted_date) = (?)
            WHERE 
                node_id = (?)
        """
        self.sql_worker.insert_query_runner(q_sql_add_log, data=[d,id])
        print("sql add success.", end='\n')
        
        
    
    
     
if __name__ == '__main__':
    d = DomainExtractorAgent()
    d.orchestrator()