import requests, json
from graph_constructor import Constructor

class EnvVariables:

    """
    Initializing env variables
    """

    t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJpYXQiOjE2MzcxNDI2NjZ9.AkLL2rMRyvSkRoWEg2qbMMvv28-Y94-Hth4Qyh5Nl4c"

    base_url = "https://api.prod.sb.codebuckets.in/v3/"
    auth = 'auth/oauth'
    me = ''

    # payload to get the messages as a response
    payload = {
        "last_id": 0,
        "selectedIndex": 0,
        "token": t
    }

class ApiDataExtractor:
    
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



a = ApiDataExtractor()

