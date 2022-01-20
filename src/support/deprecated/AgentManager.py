
class AgentManager:
    
    """
    Acts on a thought block in some capacity
    Takes as an input a single (or multiple) thought blocks
    and outputs its own block enhancer
    
    parameters:
    input: the thought that the work is being done on 
    include chain: flag, only consider the base block or the chain as well 
    error: the prediction error (or processing error, how confident is the system in the act)
    """
    
    def __init__(self, thought):
        self.input = thought
        self.error = None       # generates the error in its output that can then be cascaded upward or downward for chained skills 
        self.output = None
        self.skill = None