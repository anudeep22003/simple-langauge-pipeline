import requests, json
from neo4j_interfacer import Constructor
from env_variables import EnvVariables



class ApiDataExtractor:
    
    """
    Get the data out from Sidebrain's backed via an API and use it to construct the graph.
    
    Functions:
    - Init
        environment variables, object of constructor class and calls the orchestrator function
    - requester
        calls the api to get the data out, 
        and converts the str to json object using the requests objects inbuilt json method
    - orchestrator 
        (1) handles the API pagination and has a stop flag which stops after page 1 run. 
        (2) takes the requestors json data output and goes thread by thread to construct graph
        (3) dumps the json to a file (may help to have all data in a single json)
            write to the file by loading the file's current json into a python object and then 
            extending it with the current API response, then truncating the file and rewriting it. 
    """
    
    
    def __init__(self) -> None:
        self.url = EnvVariables.base_url
        self.body = EnvVariables.payload
        self.constructor = Constructor()
        self.orchestrator()
        pass
    
    def requester(self, page = 0, page_size = 20):
        self.body['last_id']=(page*page_size)
        response = requests.post(url=self.url, data=self.body)
        response_obj = response.json()
        data = response_obj['data']
        return data 

    def orchestrator(self, stop = 0):
        page = 0
        data = self.requester(page = 0)
        while len(data) != 0 and stop == 0:
            print(f"Run of page #{page} started.\n")
            for thread in data:
                self.constructor.thread_parser(thread)
            # try: run graph constructor 
            # except: print page, id and parent_id of failed message 

            with open(file='src/knowledge_graph/anudeep_braindump.json',mode='a') as f:
                try:
                    py_obj = json.load(fp=f)
                except:
                    py_obj = []
                
                py_obj.extend(data)
                f.truncate(0)
                json.dump(py_obj, fp=f)
            
            print(f"Run of page #{page} completed.\n")
            
            page+=1
            # stop = 1 # use this to stop after the first run
            data = self.requester(page = page)





