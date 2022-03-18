from abstract_factory import Command, CommandHandler

class KeywordExplorerCommand(Command):
    
    """
    This allows you to explore the keywords
    requirement; 
    - POS
    - the word / token 
    - label type (or none)
    
    Returns:
    - connected keywords 
    - connected threads 
    
    
    """
    
    def __init__(self, word, local_command_handler:CommandHandler)  -> None:
        pass
    
    
    pass
