import pandas as pd
from pandas.core.algorithms import mode
import json

def csv_loader(filename = 'test.json', dest_filename = 'messages.csv'):
    with open(file=filename,mode='r') as f:
        df = pd.json_normalize(f)
        #print(df)
        df.to_csv(dest_filename)

def json_loader():
    with open('test.json') as f:
        data = json.load(f)
        len(data)

def csv_reader():
    df = pd.read_csv('messages.csv')
    print(df[:5])

csv_reader()