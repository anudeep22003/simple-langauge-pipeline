# Knowledge graph input logic

Thread Structure
- id
- type
- parent_id
- Updated_at
- idd
- data
    - ink_title
    - link_img
    - coords
    - uri

children
- child 1 ( meta data especially the title)
- child 2 ( any data that I may have personally inputted )
- [thread1, thread2, .....]
- thread [parent( data-> uri, metadata img, title, coords), children: [child1, child2]]

### Cases

- Link
    - child metadata 

- Link 
    - child metadata
    - (one or more) user added children 

- Link
    - child metadata + included personally added data (no clear idea of how to separate)

- text parent
    - child parent (no meta data)

- text parent
    - text children 
    - thread links (does this have metadata as a separate message?)

Link 
    - child metadata 
    - child links 
    - (does this have metadata in links?)
    - child texts


## Final Data Structue we are working with:

entry point: list of threads
- [thread1, thread2, thread3,.....]
struct of thread:
- [message, children [message1, message2,....]]
struct of message:
- [id, type, parent_id, updated_at, idd, data: [link_title, link_img, coords, uri]]
Cases in the thread:
    - (type == link) --> the uri will contain the link and the metadata will be contained in the link_title, link_img
    - (type == text) --> uri will contain text and link_title and link_img will be NULL

If children exist
- struct is [child1, child2, ......]
- each child is structured the same as message @line54


 ## Logic




### V2 logic


def parent_node_creator(msg: dict):
    q = f"""
    merge (:Parent :Message {{
    id: "{msg['id']}",
    type: "{msg['type']}",
    updated_at: datetime("{msg['updated_at']}"),
    idd: {msg['idd']},
    uri: {msg['data']['uri']}
    }})
    """

- run_cypher(q)

    if msg['data']:
        meta_node_creator(msg['data'], msg['id'])        



def meta_node_creator(data: dict, id: str):
    q = f"""

    merge (m :Meta {{
    title: "{data['link_title']}",
    img: "{data['link_img']}",
    coords: "{data['coords']}"
    }})

    with m
    match (msg :Message)
    where msg.id = id
    merge (msg)-[:HAS_META]->(m)
    """

  - run_cypher(q)



def child_node_creator(msg: dict):
    q = f"""
    merge (c :Child :Message {{
    id: "{msg['id']}",
    type: "{msg['type']}",
    parent_id: {msg['parent_id']},
    updated_at: datetime("{msg['updated_at']}"),
    idd: {msg['idd']},
    uri: "{msg['data']['uri']}"
    }})
    
    with c
    match (p :Parent)
    where p.id = c.parent_id
    merge (p)-[:HAS_CHILD]->(c)
    """

    if msg['data']:
        meta_node_creator(msg['data'], msg['id'])

def cypher_runner(query):
    cypher.execute()

def cypher_logger():
    pass




for thread in threads:
      + create message node (parent_creator function)
      + assign :Parent :Message label
      case: NOT (msg['data']['link_title']= "" or msg['data']['link_img] == NULL)
          + create meta node
          + match message_node where message_node.id = msg['id']
          + join (message)-[:HAS_META]->(meta)
      case: 'children' in msg.keys():
          for msg in threads:
            + create message node
            + assign :Child label 
            + match parent on p.id = child.parent_id
            + join (parent)-[:HAS_CHILD]->(child)
            case: NOT (msg['link_title]= "" or msg['link_img] == NULL)
                + create meta node
                + match message_node where message_node.id = msg['id']
                + join (message)-[:HAS_META]->(meta)














### V1 logic

"""
Building entire Cypher queries sequentially 
While the query buoilding worked, the problem with this approach was 
needing to remember the original parent node for all the subsequent merge clauses 
Which meant that every message of a thread had to be dumped into a single cypher query
I realized it would be easier for each node to be created independently 
and if there are any relationships to be created, use a match clause
this way every its not an all or nothing, but creation happening at every step
"""

def merge_parent_query_builder(message_dict: dict, labels: list):
   query = f"""merge ({} {} {
    id: "{}",
    type: "{}",
    updated_at: datetime("{}"),
    idd: "{}",
    uri: "{}"
    """.(
        "parent_node",
        + label_generator(labels),
        message_dict['id'],
        message_dict['type'],
        message_dict['updated_at'],
        message_dict['idd'],
        message_dict['uri']
        )
    })
    return query

def label_generator(labels: list):
    q = ""
    for label in labels:
        q+=f" :{}".(label)
    return q

def merge_child_query_builder(message_dict: dict, labels: list):
    return merge_parent_query_builder(message_dict, labels)[-2:] + f",parent_id: {} })".(message_dict[parent_id])




def msg_dict_parser(message_dict):
    for msg in threads:
        + create message node
        + assign parent label
        case: NOT (msg['link_title]= "" or msg['link_img] == NULL)
            + create meta node
            + join (message)-[:HAS_META]->(meta)

    return cypher_query

for thread in threads:
    for msg_dict in thread:
        + create message node
        + assign parent label
        case: NOT (msg['data']['link_title']= "" or msg['data']['link_img] == NULL)
            + create meta node
            + join (message)-[:HAS_META]->(meta)
        case: NOT (msg['children'] throws exception: KeyError):
            for msg in threads:
              + create message node
              + assign parent label
              case: NOT (msg['link_title]= "" or msg['link_img] == NULL)
                  + create meta node
                  + join (message)-[:HAS_META]->(meta)

