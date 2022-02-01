import sqlite3 

# create a connection object that represents the database
# the database sample.db will be created and subsequent data will be stored in here
con = sqlite3.connect('sample.db')

# the cursor object is akin to a cursor from where you can run SQL commands
cur = con.cursor()

# CREATE TABLE
cur.execute(''' DROP TABLE IF EXISTS messages
''')

cur.execute(''' CREATE TABLE IF NOT EXISTS messages 
    (d_coords text,
    d_link_img text,
    d_link_title text,
    d_uri text,
    id text,
    idd real,
    parent_id text,
    type text,
    updated_at text)
''')

cur.execute(""" CREATE TABLE IF NOT EXISTS sample_person 
(name, lastname, age, sex)
""")

cur.execute(''' INSERT INTO sample_person VALUES  ('Deanna', 'Takasugi', 28, 'F')
''')

con.commit()

for row in cur.execute(''' SELECT * from sample_person'''):
    print(row)