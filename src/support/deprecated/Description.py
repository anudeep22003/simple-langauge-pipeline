class Description:
    
    """
    Would like to come up with a better name but this is the associative deconstruction of the payload provided by the brain. 
    In simpler terms, it is a description of what was useful or meaningful about the block that the user just added. 
    This is an optional field, although we should convince the user to add this \
    because it makes a huge difference to our ability to organize their knowledge.
    """
    
    def __init__(self, content):
        self.description = content
    
    
    def print_attributes(self):
        print(f"{'description':15} {self.description}")
    
    pass
    