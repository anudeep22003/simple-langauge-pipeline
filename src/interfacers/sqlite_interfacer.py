from datetime import datetime
import sqlite3
from typing import final
from datetime import datetime



class SqlHandler:
    CON = sqlite3.connect("src/data/personal.db", \
                      detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    
    def __init__(self) -> None:
        self.cursor = SqlHandler.CON.cursor()
        self.record = 0
        self.initialize_db()
        self.limiter = 0
        pass
    
    def initialize_db(self):
        
        q_drop = "Drop table if exists message_index"
        self.write_query_runner(q_drop)
        
        q_create_message_table = "\
        CREATE TABLE IF NOT EXISTS message_index (\
        node_id INTEGER NOT NULL PRIMARY KEY,\
        node_labels TEXT,\
        loading_date DATETIME,\
        keyword_extracted_date DATETIME,\
        node_edited_date DATETIME,\
        uri TEXT\
        ) WITHOUT ROWID"
        self.write_query_runner(q_create_message_table)

        q_drop = "Drop table if exists meta_index"
        self.write_query_runner(q_drop)
        
        
        q_create_meta_table = "\
            CREATE TABLE IF NOT EXISTS meta_index (\
            node_id INTEGER NOT NULL PRIMARY KEY,\
            node_labels TEXT,\
            loading_date DATETIME,\
            keyword_extracted_date DATETIME,\
            title TEXT,\
            img text\
            ) WITHOUT ROWID\
        "
        self.write_query_runner(q_create_meta_table)
        
        pass
        

        
    def write_query_runner(self, query):
        try:    
            self.cursor.execute(query)
        finally:
            SqlHandler.CON.commit()
        
        pass

    def insert_query_runner(self, query: str, data: list):        
        
        try: 
            # print(f"Query: \t{query} \n data-type: {type(data)} \tdata: {data} ")
            self.cursor.execute(query,data)
            print(f"insert #{self.record} succesful")
            self.record+=1
        except:
            print("Exception caught executemany block")
        finally:
            SqlHandler.CON.commit()
                    
        pass
    
    def insert_query_generator(self, label: str):
        if label == "Message":
            q_insert_message = "\
            INSERT INTO message_index (\
                node_id, node_labels, loading_date, keyword_extracted_date,\
                node_edited_date, uri)\
                VALUES (?,?,?,?,?,?)\
            "
            return q_insert_message

        elif label == "Meta":
            q_insert_meta = "\
            INSERT INTO meta_index (\
                node_id, node_labels, loading_date, keyword_extracted_date,\
                title, img)\
                VALUES (?,?,?,?,?,?)\
            "
            return q_insert_meta

        else:
            print("Unexpected Label")


if __name__  == "__main__":
    s = SqlHandler()
    # q = "INSERT INTO message_index (node_id, node_labels, loading_date, keyword_extracted_date, node_edited_date, uri) VALUES (?,?,?,?,?,?)"
    # data = [5, str(['Message', 'Parent']), datetime(2022, 2, 1, 12, 31, 49, 139850), datetime(2022, 2, 1, 12, 31, 49, 139851), datetime(2022, 2, 1, 12, 31, 49, 139851), 'https://www.reddit.com/r/askscience/comments/q1xw1t/if_the_higgs_field_gives_mass_to_matter_and_the/?utm_source=share&utm_medium=mweb'] 
    # s.insert_query_runner(q,data)
    pass