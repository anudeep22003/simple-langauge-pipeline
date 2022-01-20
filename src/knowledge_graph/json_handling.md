# Working with JSON

structure of the json:

good response:
- status: "success"
- data: [dict, dict, dict]
  - dict: a single thread
    - id: ", ..... data; dict
    - children: []

bad response:
- status: "success' / "failure"
- data: [] (empty list)

How we work with a json
- request.post(url, data) -> response object 
- response.text is a string 
- convert string to a python object
- store only the 'data' value in the dict 
  - list: [dict, dict, dict]
run following subprocesses --> while len(response) != 0:
  - try (run graph constructor on that page's result ) except: (print the start_page, id and parent_id of the failed message)
  - when completed, 
    - json.load('anudeep_braindump.json') --> file containing the json dumped so far 
    - append the current page list 
    - json.dump and rewrite onto the same json file 
  - start_page+=20

Options:
- store the entire json first then construct graph out of it 
- (winner) construct graph out of each page as the response streams, then store to json obj at the end 
  - (adv) easier to identify vicinity of failure
  - (adv) supports the philosphy of not having one long tunnel but rather many short ones  


------------- working with json -------------

Json.dump --> convert a py object into a json object
- json.dump (if file) 
- json.dumps (if string)

json.load --> convert a json object to a python object 
- json.load (if file)
- json.loads (if string)