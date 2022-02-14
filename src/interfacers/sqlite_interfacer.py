import sqlite3
from datetime import datetime
import sys

import os, sys
sys.path.append(os.path.join(os.getcwd(),'src','glial_code'))
from decorators import Decorators



class SqlInitializer:
    
    """
    Purpose: 
    
    To initilaize a sqllite databases by: 
    - Emptying it if it already exists
    - Creating tables with the primary key, column_names and repsective datatypes (message_index and meta_index currently)
    - Generate queries to insert data into each respective table
    
    """
    
    def __init__(self) -> None:
        # self.cursor = SqlInterfacer.CON.cursor()
        # self.write_query_runner = SqlInterfacer.WRITE_QUERY_RUNNER()
        # self.insert_query_runner = SqlInterfacer.INSERT_QUERY_RUNNER()
        self.record = 0
        self.initialize_db()
        self.limiter = 0
        pass
    
    def clear_db(self):
        q_drop = "Drop table if exists message_index"
        SqlInterfacer.WRITE_QUERY_RUNNER(q_drop)

        q_drop = "Drop table if exists meta_index"
        SqlInterfacer.WRITE_QUERY_RUNNER(q_drop)
        
    
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
            domain_extracted_date DATETIME\
            ) WITHOUT ROWID"
            SqlInterfacer.WRITE_QUERY_RUNNER(q_create_message_table)
            
            
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
            SqlInterfacer.WRITE_QUERY_RUNNER(q_create_meta_table)
        else:
            pass
        
    def add_column(self):
        q = f"""ALTER TABLE message_index
                ADD domain_extracted_date DATETIME
        """
        SqlInterfacer.WRITE_QUERY_RUNNER(q)

    
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


@Decorators.singleton
class SqlInterfacer:
    
    """
    Global Variables:
    CON --> A connection to the sqlite database
    CURSOR --> a cursor of the connection that allows to read and write queries.
    INSERT_RECORD, WRITE_RECORD, EXTRACT_RECORD --> variables to keep track of number of entries
    
    Purpose:
    A single class to interface with the sqlite database, currenlty includes reading and writing to database. 
    
    ******* Functions: ********
    - WRITE_QUERY_RUNNER
    (1) Takes a query as an input and writes it to the db and commits at the end. 
    (2) Does not take any data as input and is primarly focused on initializing functions. 
    
    - INSERT_QUERY_RUNNER
    Takes an insert query and corresponding well-formed data as an input and writes it to the db, and commits at the end. 
    
    - READ_QUERY_RUNNER
    Takes a read query, runs it and returns the cursor object and consolidates all the queried rows into a single list to return. 
    
    - TEST_READ_QUERY_RUNNER
    Created to help with debugging the rest of the functions. 
    
    """
    
    def __init__(self) -> None:    
        self.con = sqlite3.connect("src/data/personal.db", \
                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.con.cursor()
        self.insert_record = 0
        self.write_record = 0
        self.extract_record = 0
        
    
    def write_query_runner(self, query):
        try:    
            self.cursor.execute(query)
            self.write_record+=1
            print(f"insert #{self.write_record} succesful")
        finally:
            self.con.commit()


    def insert_query_runner(self, query: str, data: list):

        try: 
            # print(f"Query: \t{query} \n data-type: {type(data)} \tdata: {data} ")
            self.cursor.execute(query,data)
            print(f"insert #{self.insert_record} succesful")
            self.insert_record+=1
        except Exception as e:
            print(f"Exception caught: {type(e)}\t str: {e.__str__} args: {e.args}")
        finally:
            self.con.commit()
    
    
    def read_query_runner(self, query:str):
        try:
            return self.cursor.execute(query).fetchall()
        except Exception as e:
            print(f"Exception caught: {type(e)!r}\t args: {e.args}")
        
    
    def test_read_query_runner(self):
        
        query = """Select * from message_index 
               where node_labels like '%Child%' 
               limit 10
               
               """
        
        try:
            l = self.read_query_runner(query)
            print(f"type: {type(l)}\tlength: {len(l)}")
            #print(l, end='\n')
            print("---"*10,end='\n')
            for index in range(10):
                print(f"label: {str(l[index][1]):<20s}\t uri: {l[index][5]}")
            
        except Exception as e:
            print(f"Exception caught: {type(e)}\t str: {e.__str__} args: {e.args}")
        pass
    
    #@catch_exception
    def tester(self, query = """Select * from message_index 
               where node_labels like '%Child%' 
               limit 10
               
               """):
        return self.cursor.execute(query).fetchall()
                    
    
    


if __name__  == "__main__":
    s = SqlInitializer()
    # q = "INSERT INTO message_index (node_id, node_labels, loading_date, keyword_extracted_date, node_edited_date, uri) VALUES (?,?,?,?,?,?)"
    # data = [234445, str(['Message', 'Parent']), datetime(2022, 2, 1, 12, 31, 49, 139850), datetime(2022, 2, 1, 12, 31, 49, 139851), datetime(2022, 2, 1, 12, 31, 49, 139851), 'https://www.reddit.com/r/askscience/comments/q1xw1t/if_the_higgs_field_gives_mass_to_matter_and_the/?utm_source=share&utm_medium=mweb'] 
    #SqlInterfacer.TEST_READ_QUERY_RUNNER()
    s.add_column()
    pass



