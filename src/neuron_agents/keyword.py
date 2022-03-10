# Python imports
import functools, re, sys, os, json, time, matplotlib.pyplot as plt
from collections import Counter
import spacy


# internal imports
from connector import Connector

sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from sqlite_interfacer import SqlInterfacer 
from neo4j_interfacer import Neo4jInterfacer

sys.path.append(os.path.join(os.getcwd(),'src','glial_code'))
from decorators import Decorators

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe("textrank")


def sample_func():
    doc = nlp("How to write singleton classes in Python, i.e. classes where only a single instance is allowed to be created.")

    print(type(doc))



    def write_decorator(func):
        "Writes the output to a file"
        @functools.wraps(func)
        def writer(*args, **kwargs):
            with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/spacy_op.txt", mode='a') as f:
                f.write(f"FUNC: {func.__name__}:\n"+str(func(*args, **kwargs))+"\n"+ "---"*25 +"\n")
        return writer

    @write_decorator
    def noun_printer(doc):
        return [nc for nc in doc.noun_chunks]

    #noun_printer(doc)
    #token_printer_no_stop(doc)

    @write_decorator
    def token_printer_no_stop(doc):
        return [return_one_by_one(t) for t in doc if not t.is_stop]

    @write_decorator
    def dep_printer(doc):
        return [return_one_by_one(token, token.dep_,token.head.text, token.head.pos_, [child for child in token.children]) for token in doc]

    #doc = nlp("A video of Nancy's brain being zapped by Transcranial Mangnetic Simulation")

    @write_decorator
    def return_one_by_one(*args):
        return args

    #noun_printer(doc)
    #token_printer_no_stop(doc)
    #dep_printer(doc)

    def f():
        doc = nlp("A course by ex-Google and Facebook engineers and also BITs Pilani and Georgia Tech educated, on state of art NLP.")

        print("{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^20s}\t{:^15s}".format("token","ent","dep", "head"," pos"," children","is stop?"))
        print("-"*120,end='\n')
        for t in doc:
            print("{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^20s}\t{:^15s}".format(t.text, 
                                                                            str([(ent.label_,t.ent_iob) for ent in doc.ents if ent.text == t.text]), 
                                                                            t.dep_, 
                                                                            t.head.text, 
                                                                            t.head.pos_, 
                                                                            str([child for child in t.children]),
                                                                            ('X' if t.is_stop else "")))
        print("-"*120,end='\n')

class KeywordSampler:
    
    """
    
    go through the following columns and extract out the data as follows
    - content
    - url extracted content
    - remaining text 
    - ignored words
    - nouns
    - ents
    - nouns
    - dependencies
    
    Procedure:
    - Make a pass through uri column in sql table 
    - leave url scrapped portion of the text 
    - run the text through spacy pipeline
    - maintain a main list of dict at the class level (to dump to a json)
    - use a template dict to add info to, 
    - append returned dict to the main dict list
    - at the end write the list to a txt json file
    
    Functions:
    
    re_subber
    - returns the input string after replacing all url occurences in it with an empty string. 
    
    template
    - returns a shaped dict to add the string output to
    
    """
    
    
    def __init__(self) -> None:
        self.dump = []
        self.sql = SqlInterfacer()
        self.url_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')
        self.run_time = []
        self.write_time=[]
        pass
    
    def template_dict(self):
        return {
            "content": "",
            "url_extracted_content": "",
            "diff_score":"",
            "stop_tokens": [],
            "nouns": [],
            "noun_lemmas": [],
            "adjectives": [],
            "adjective_lemmas": [],
            "proper_nouns":[],
            "verbs":[],
            "verb_lemmas": [],
            "noun_chunks": [],
            "ents": [],
            "phrases":[],
            "phrase_chunks":[]
            # "dependencies": []x
        }
    
    
    def orchestrator(self):
        for entry in self.sql_extractor():
            string = "".join([e for e in entry])
            scrubbed_text = self.re_subber(string).lower()
            if scrubbed_text:
                self.dump.append(self.parse_text(string,scrubbed_text))
        
        self.writer()
        
        fig,ax = plt.subplots()
        ax.plot(range(len(self.run_time)), self.run_time)
        plt.yscale("log")
        plt.show()
        
        # pp(self.dump)
    
    def writer(self):
        with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/extracted_keyword_analyzer_lower.json", mode='a') as f:
            json.dump(self.dump,f)
    
    
    
    def lemmatized_text_parser():
        pass    

#    @Decorators.timer
    def parse_text(self,entry,scrubbed_text):
        start_time = time.perf_counter()   
        d = self.template_dict()
            
        d['content'] = entry
        
        # extract url 
        d['url_extracted_content'] = scrubbed_text
        d['diff_score'] = len(scrubbed_text)*100/len(entry)
        
        # spacy processing 
        doc = nlp(scrubbed_text)
        for token in doc:
            if token.is_stop:
                d['stop_tokens'].append(token.text)
            if token.pos_ == 'NOUN':
                d['nouns'].append(token.text)
                d['noun_lemmas'].append(token.lemma_)
            if token.pos_ == 'PROPN':
                d['proper_nouns'].append(token.text)
            if token.pos_ == 'VERB':
                d['verbs'].append(token.text)
                d['verb_lemmas'].append(token.lemma_)
            if token.pos_ == 'ADJ':
                d["adjectives"].append(token.text)
                d['adjective_lemmas'].append(token.lemma_)
            
            #d['pos'].append((token.text, token.pos_))    
        
        d['ents'].extend([(ent.text,ent.label_) for ent in doc.ents])
        d['noun_chunks'].extend([chunk.text for chunk in doc.noun_chunks])
        
        for phrase in doc._.phrases:
            d['phrases'].append((phrase.text, phrase.rank, phrase.count))
            for t in phrase.chunks:
                d['phrase_chunks'].append((t.text))    
        
        end_time = time.perf_counter()      # 2
        self.run_time.append(end_time - start_time)    # 3
        return d
    
    
    def aggregate_statizer(self):
        
        """
        go through the json and write to a dict {token: frequency}:
        - propn
        - nouns
        - verbs
        - adj
        - ents
        """
        
        with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/extracted_keyword_analyzer_lower.json",mode='r') as f:
            full_dict = json.load(f)
        
        file_name = [
            'nouns',
            'adjectives',
            'verbs',
            'proper_nouns',
            'ents',
            'phrases',
            'noun_chunks',
            'noun_lemmas',
            'verb_lemmas',
            'adjective_lemmas',
            'overall_lemmas'
        ]
        
        counter_list = [Counter(),Counter(),Counter(),Counter(),Counter(),Counter(),Counter(),Counter(),Counter(),Counter(),Counter()]
        
        for d in full_dict:
                
            t_s = time.perf_counter()
            for word in d['nouns']:
                counter_list[0][word]+=1

            for word in d['adjectives']:
                counter_list[1][word]+=1

            for word in d['verbs']:
                counter_list[2][word]+=1

            for word in d['proper_nouns']:
                counter_list[3][word]+=1

            for word,_ in d['ents']:
                counter_list[4][word]+=1
            
            for word,_,_ in d['phrases']:
                counter_list[5][word]+=1

            for word in d['noun_chunks']:
                counter_list[6][word]+=1
            
            for word in d['noun_lemmas']:
                counter_list[7][word]+=1
                counter_list[10][word]+=1
            
            
            for word in d['verb_lemmas']:
                counter_list[8][word]+=1
                counter_list[10][word]+=1
            
            
            for word in d['adjective_lemmas']:
                counter_list[9][word]+=1
                counter_list[10][word]+=1
            
            
            t_e = time.perf_counter()
            self.write_time.append(t_e-t_s)
        
        for i,counter in enumerate(counter_list):
            t_s = time.perf_counter()        
            with open(f"/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/keyword_aggregates/{file_name[i]}.json", mode='a') as f:
                json.dump(dict(counter.most_common()),f)
            t_e = time.perf_counter()
            print(f"wrote to file#{i} in {str(t_e-t_s)} sec")
        
        fig,ax = plt.subplots()
        ax.plot(range(len(self.write_time)), self.write_time)
        plt.yscale("log")
        plt.show()
    
    
    def sql_extractor(self):
        return self.sql.read_query_runner("SELECT uri FROM message_index")
    
    def re_subber(self, s):
        return re.sub(self.url_pattern,"",str(s))
        
        pass
    
    pass


class KeywordExtractor:
    
    """
    Extract keywords from the text passed to it, and merge into the neo4j graph. 
    
    Process:
    - extract data from sql 
    - remove url occurences 
    - run spacy tokenizer on extracted text 
    - for every lineitem, construct keyword list 
    - merge the keywords into the neo4j graph
    
    ##### Functions #####
    
    - 
    
    
    
    
    """
    
    def __init__(self, 
                 tables:list = ['Message','Meta']) -> None:
        self.sql = SqlInterfacer()
        self.neo = Neo4jInterfacer()
        self.connector = Connector()
        self.tables = tables
        self.url_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')
        pass
            
            
    def general_orchestrator(self):
        for source_table in self.tables:
            for (id_start,textstring) in self.extract_sql_data_general(source_table):
                
                scrubbed_textstring = self.remove_urls(textstring)
                scrubbed_textstring = scrubbed_textstring.lower()
                
                if scrubbed_textstring:
                    d = self.extract_token(scrubbed_textstring)
                    for pos,token_list in d.items():
                        if len(token_list) != 0:
                            for token in token_list:
                                id_end = self.create_general_node(pos,token)
                                self.connect_general_token_in_graph(id_start, id_end, pos, source_table)
            
            
        
    def extract_sql_data_general(self, source):
        if source == 'Message':
            return self.sql.read_query_runner("SELECT node_id, uri FROM message_index")
        elif source == 'Meta':
            return self.sql.read_query_runner("SELECT node_id, title FROM meta_index")
    
    
    def remove_urls(self, text: str):
        return re.sub(self.url_pattern, "", text)
            
    def dict_constructor_general(self, id_start: int, id_end: int, pos: str, table: str):
        return {
            "start_node": id_start,
            "end_node": id_end,
            "r_name": pos,
            "r_direction_towards":"end",
            "r_properties": {"type": pos, "source": table}
        }    
    
    def extract_token(self, text: str):
        doc = nlp(text)
        d = {'VERB': [], 
             'ADJ': [], 
             'NOUN':[]}
        for token in doc:
            if token.pos_ in d.keys():
                d[token.pos_].append(token.text)

        return d    
    
    def create_general_node(self, keyword_pos: str, keyword_token: str):
        q = f"""MERGE (k:Keyword:{keyword_pos} {{word: "{keyword_token}"}})
        return id(k) as id
        """
        return_object = self.neo.cypher_write_read_query_runner(q)
        return return_object[0]['id']
    
    
    def connect_general_token_in_graph(self, id_start, id_end, pos, source_table):
        self.connector.orchestrator(self.dict_constructor_general(id_start, id_end, pos, source_table))
        pass






if __name__=="__main__":
    
    k = KeywordExtractor()
    k.general_orchestrator()