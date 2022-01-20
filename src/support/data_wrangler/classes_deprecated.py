import csv
import requests
import json
from pprint import pprint
import pandas as pd
from csv import DictWriter


# initializing a fixed token
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

    msg_keys = ['id', 'type', 'parent_id', 'updated_at', 'idd', 'data']
    csv_keys = [
        'd_coords', 'd_link_img', 'd_link_title', 'd_uri', 'id', 'idd', 'parent_id', 'type', 'updated_at'
    ]

class Parser:
    """
    The class where the parsing of the JSON string happens
    """    
    
    def __init__(self) -> None:
        
        self.keys = self.thread_keys()
        self.thread_list = []
        #self.thread_parse_handler()
    
    
    
    """
    Action Functions that make changes to values without returning
    """

    def thread_parse_handler(self, payload):
        
        self.thread_list = []

        # parse thread by thread
        for thread in payload:
            self.thread_parser(thread)
            
            # check if there are any children keys

            try:
                thread['children']
            except KeyError:
                #print("This thread has no children")
                continue
            
            for child in thread['children']:
                self.thread_parser(child)
        
        return self.thread_list


    def thread_parser(self, thread):
        
        thread_dict = {}

        for key in self.keys:
                
                # if key is data, then update the dict with the returned dict from 
                # data parser subroutine
                if key == 'data':
                    thread_dict.update(self.data_parser(thread[key]))
                else:
                    thread_dict[key] = thread[key]
            
        self.thread_list.append(thread_dict)


    """
    Return functions, ones that take an input do something and return a value
    """
    
    def data_parser(self,data_payload):
        data_dict = {}
        for key in data_payload.keys():
            data_dict["d_{}".format(key)] = data_payload[key]
        return data_dict

    # as much as i dislike it, for MVP we are hardcoding the keys
    def thread_keys(self):
        msg_keys = ['id', 'type', 'parent_id', 'updated_at', 'idd', 'data']
        return msg_keys


class Orchestrator(EnvVariables):

    """

    """

    def __init__(self) -> None:
        self.url = EnvVariables.base_url
        self.payload = EnvVariables.payload
        self.parser = Parser()
        self.orchestrate()
        pass

    def orchestrate(self):
        
        """
        what runs the orchestrator from inside, and handles pagination when necessary. 
        """
        
        start_index = 0
        valid_flag = True
        length = 1

        
        while valid_flag and length != 0:
            
            valid_flag, jsonstring = self.api_requester(start_index)
            print(f"valid run #{start_index/25:n}")
            parsed_json = self.request_translator(jsonstring)
            thread_list = self.parser.thread_parse_handler(parsed_json)
            self.csvwriter(thread_list)
            #self.filewriter(thread_list)
            #self.sql_loader(thread_list)
            #pprint(thread_list)

            length = len(thread_list)
            #print(f"\n-------------------------- # threads  = {length} -------------------------\n")
            # call the next page 
            start_index+=25
            
        

    def api_requester(self, start_index = 0):
        
        """
        makes the actual api request
        """
        self.payload['last_id']=start_index
        response = requests.post(url = self.url, data = self.payload)
        #print(f"status code: {response.status_code}")
        return response.status_code == 200, response.text

    def request_translator(self, jsonstring):
        
        """ 
        takes the response from api requester, 
        - filters the data key 
        - json loads converts to python recognizable objects 
        """
        translated_response = json.loads(jsonstring)
        return translated_response['data']


    
    def csvwriter(self, thread_list):
        
        with open('messages.csv','a') as f:
                writer = DictWriter(f,fieldnames=EnvVariables.csv_keys)
                for dic in thread_list:
                    writer.writerow(dic)
        pass

    def filewriter(self, thread_list):
        
        with open("test.json", mode='a') as f:
            for dic in thread_list:
                json.dump(dic, f, separators=(',',':'))
            pass
    
    #! this is not working and hence unused.     
    def sql_loader(self, thread_list):
        cur = self.con.cursor()
        while cur:
            cur.executemany("INSERT INTO messages VALUES (:d_coords, :d_link_img, :d_link_title, :d_uri, :id, :idd, :parent_id, :type, :updated_at)", thread_list)
        self.con.commit()
        pass



print("before run")

o = Orchestrator()

print("after run")



