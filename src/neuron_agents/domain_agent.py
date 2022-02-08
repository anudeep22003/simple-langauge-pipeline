import re, sys
from tld import get_tld
import os
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))

from sqlite_interfacer import SqlInterfacer


#from interfacers.sqlite_interfacer import SqlInterfacer


# def re_extractor():

#     url_re_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')

    
    
    
#     for t in re.findall(url_re_pattern, q):
#         print(t, len(t))
        
#     with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/cypher_to_sql_meta.txt",mode='r') as f:
#         for line in f.readlines():
#             print(re.search(pattern,line))

    
#    pass


#re_extractor()


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
    - merge a node into the graph 
    - use the id to reference to the node being processed
        - connect the merged node to referenced using a [:DOMAIN_OF] and [:SUBDOMAIN_OF] relationship
    - add datetime.now to sql column 'domain extracted date'
    """
    def __init__(self) -> None:
        self.url_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')
        pass
    
    def query_generator(self):
        return "Select node_id, uri from message_index limit 100"
    
    def query_executor(self, query:str):
        #print([r for r in SqlInterfacer.READ_QUERY_RUNNER(query)])
        return SqlInterfacer.READ_QUERY_RUNNER(query)
    
    def orchestrator(self):
         for row in self.query_executor(self.query_generator()):
             id = row[0]
             for match in self.url_extractor(row[1]):
                self.url_parser(url=match[0])
    
    def url_extractor(self, string_to_process:str):
        return re.findall(self.url_pattern, string_to_process)
    
    def url_parser(self,url):
        res = get_tld(url, as_object=True)
        self.writer("res: {:<15s}\tsubdomain: {:<10s}\tdomain: {:<20s}\ttld: {:<10s}\tfld: {:<25s}\turl: {:<s}\n".format(str(res), str(res.subdomain), str(res.domain), str(res.tld), str(res.fld), url))
    
    def writer(self, content):
        with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/extracted_urls.txt", mode='a') as f:
            f.write(content)
        pass

if __name__ == '__main__':
    d = DomainExtractorAgent()
    d.orchestrator()