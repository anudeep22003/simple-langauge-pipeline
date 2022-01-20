from Description import *
from Payload import *
import random

class ThoughtBlock:
    
    """
    Would contain the payload and the natural language description of the content
    
    parameters:
    payload: the media that is the source of the new thought 
    description: what the user finds useful - a deconstruction of the associations made by the brain
    """
    
    def __init__(self, media, description):
        
        # todo = convert to a uuid
        self.id = random.randint(0,1E9)
        self.p = Payload(media)
        self.d = Description(description)
        
    def print_attributes(self):
        self.p.print_attributes()
        self.d.print_attributes()
    
    pass


