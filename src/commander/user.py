from command_handler import UserCommandHandler
import random, string

class User:
    
    """
    To instantiate and store users. 
    
    Cool things you can do:
    - Add a different neo4j url_location for each user
    - each user has their own command handler
    """
    
    
    def __init__(self, name, 
                 id: str = None, 
                 loc: str = 'Bangalore', 
                 command_handler = UserCommandHandler) -> None:
        
        self.name = name
        self.id = self.generate_id(id)
        self.loc = loc 
        self.command_handler = command_handler()
    
    
    def generate_id(self, id):
        if id is None:
            return "".join(random.choices(string.digits, k=12))
        return id
      
    