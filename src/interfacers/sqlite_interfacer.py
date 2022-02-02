from datetime import datetime
import sqlite3
from datetime import datetime



class SqlInitializer:
    
    def __init__(self) -> None:
        # self.cursor = SqlInterfacer.CON.cursor()
        # self.write_query_runner = SqlInterfacer.write_query_runner()
        # self.insert_query_runner = SqlInterfacer.insert_query_runner()
        self.record = 0
        self.initialize_db()
        self.limiter = 0
        pass
    
    def clear_db(self):
        q_drop = "Drop table if exists message_index"
        SqlInterfacer.write_query_runner(q_drop)

        q_drop = "Drop table if exists meta_index"
        SqlInterfacer.write_query_runner(q_drop)
        
    
    def initialize_db(self, clean_slate: bool=False):
        
        if clean_slate == True:
            self.clear_db()
        
        q_create_message_table = "\
        CREATE TABLE IF NOT EXISTS message_index (\
        node_id INTEGER NOT NULL PRIMARY KEY,\
        node_labels TEXT,\
        loading_date DATETIME,\
        keyword_extracted_date DATETIME,\
        node_edited_date DATETIME,\
        uri TEXT\
        ) WITHOUT ROWID"
        SqlInterfacer.write_query_runner(q_create_message_table)
        
        
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
        SqlInterfacer.write_query_runner(q_create_meta_table)
        

    
    def insert_query_generator(self, label: str):
        if label == "Message":
            q_insert_message = "\
            INSERT OR IGNORE INTO message_index (\
                node_id, node_labels, loading_date, keyword_extracted_date,\
                node_edited_date, uri)\
                VALUES (?,?,?,?,?,?)\
            "
            return q_insert_message

        elif label == "Meta":
            q_insert_meta = "\
            INSERT OR IGNORE INTO meta_index (\
                node_id, node_labels, loading_date, keyword_extracted_date,\
                title, img)\
                VALUES (?,?,?,?,?,?)\
            "
            return q_insert_meta

        else:
            print("Unexpected Label")


class SqlInterfacer:
    CON = sqlite3.connect("src/data/personal.db", \
                      detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    CURSOR = CON.cursor()
    INSERT_RECORD = 0
    WRITE_RECORD = 0
    EXTRACT_RECORD = 0
    
    
    def write_query_runner(query):
        try:    
            SqlInterfacer.CURSOR.execute(query)
            SqlInterfacer.WRITE_RECORD+=1
            print(f"insert #{SqlInterfacer.WRITE_RECORD} succesful")
        finally:
            SqlInterfacer.CON.commit()


    def insert_query_runner(query: str, data: list):

        try: 
            # print(f"Query: \t{query} \n data-type: {type(data)} \tdata: {data} ")
            SqlInterfacer.CURSOR.execute(query,data)
            print(f"insert #{SqlInterfacer.INSERT_RECORD} succesful")
            SqlInterfacer.INSERT_RECORD+=1
        except Exception as e:
            print(f"Exception caught: {type(e)}\t str: {e.__str__} args: {e.args}")
        finally:
            SqlInterfacer.CON.commit()
    
    def read_query_runner():
        
        query = "Select * from message_index limit 2"
        
        try:
            l = SqlInterfacer.CURSOR.execute(query).fetchall()
            print(f"type: {type(l)}\tlength: {len(l)}")
            print(l, end='\n')
            print("---"*10,end='\n')
            for item in l:
                print(f"type: {type(item)}\t item: {item}")
            
        except Exception as e:
            print(f"Exception caught: {type(e)}\t str: {e.__str__} args: {e.args}")
        pass
    
    
                    
    

if __name__  == "__main__":
    #s = SqlInitializer
    # q = "INSERT INTO message_index (node_id, node_labels, loading_date, keyword_extracted_date, node_edited_date, uri) VALUES (?,?,?,?,?,?)"
    # data = [234445, str(['Message', 'Parent']), datetime(2022, 2, 1, 12, 31, 49, 139850), datetime(2022, 2, 1, 12, 31, 49, 139851), datetime(2022, 2, 1, 12, 31, 49, 139851), 'https://www.reddit.com/r/askscience/comments/q1xw1t/if_the_higgs_field_gives_mass_to_matter_and_the/?utm_source=share&utm_medium=mweb'] 
    SqlInterfacer.read_query_runner()
    pass