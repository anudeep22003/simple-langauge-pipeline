
from typing import Dict


class OntologyVariables:
    
    data_labels = {'Data': True, 'LINK': False, 'IMG': False, 'TEXT': False}
    message_labels = {'Message': True, 'parent': False, 'child': False}
    meta_labels = {'meta': True, 'retreived': False}
    

    def __init__(self) -> None:
        pass
    
    pass


class Message:
    def __init__(self, id, updated_at, coords, ntype = 'parent') -> None:
        self.properties = {'id': id, 'updated_at':updated_at, 'coords': coords}
        self.labels = Message.set_labels(ntype)

    def set_labels(ntype):
        labels = OntologyVariables.message_labels
        labels[ntype] = True
        return labels
    pass


class MetaData:
    def __init__(self, link_title, link_image) -> None:
        self.properties = {'title': link_title, 'image': link_image}
        self.labels = MetaData.set_labels()
        pass
    
    def set_labels():
        labels = OntologyVariables.meta_labels
        return labels

    pass

class Data:
    def __init__(self,payload, ntype = 'LINK') -> None:
        self.properties = {'payload': payload}
        self.labels = Data.set_labels(ntype)
        self.metadata = self.meta_generator()
        pass

    def set_labels(ntype):
        labels = OntologyVariables.data_labels
        labels[ntype] = True
        return labels
    
    def meta_generator(self):
        if self.labels['LINK'] is True:
            return MetaData()

    pass


# *Done !Fix --> Strings being added without 'quotes'
class Node:
    
    """
    boiler plate code for setting up, updating and deleting nodes
    """

    def query_builder(node):
        query = "CREATE ({} {})".format(Node.label_constructor(node.labels), Node.property_constructor(node.properties))
        print('\n\n'+query+'\n\n')
        return query

    def label_constructor(labels):
        assert isinstance(labels, Dict), "label constructor only excepts dicts"
        constructed_label_query = ''
        for k,v in labels.items():
            if v is True:
                constructed_label_query+=f':{k} '
            else:
                continue
        
        return constructed_label_query
    
    def property_constructor(property_dict):
        assert isinstance(property_dict, Dict), "property constructor only excepts dicts"
        constructed_property_query = '{'
        for k,v in property_dict.items():
            if isinstance(v,str):
                constructed_property_query+=f"{k}: '{v}',"
            else:
                constructed_property_query+=f"{k}: {v}, "
        
        # text wrangling to remove the last comma
        constructed_property_query = constructed_property_query[:-2]
        constructed_property_query+='}'

        return constructed_property_query




    pass


# Relationship Modeling

class Relation:
    """
    boiler plate code for setting up, updating and deleting connections
    """

    def connect(source_node, dir, target_node):
        
        pass

    pass


class ChildRelation:

    def __init__(self, **properties) -> None:
        
        pass

    pass

class MetaRelation:
    pass

class DataRelation:
    pass






m = Message(id=123, updated_at='hero', coords=(0,0), ntype='parent')
print(m.labels)

d = Data(payload='www.helloworld.com', ntype='LINK')
print(d.labels)

Node.query_builder(m)
