import requests
import random

class Payload:
    
    """
    This would instantiate a new payload. 
    The reason to have this as a class is that there might be verifications and checks to be peformed on the payload to ensure it is valid. 
    We will include those verifications here, although for now it is going to be a simple text field.
    
    We will have mediatype specific verifications too as this block starts taking on more responsibility. 
    """
    
    def __init__(self, media):
        self.payload = media
        self.status = self.link_verifier()
        
    
    def link_verifier(self):
        
        """
        Want this to check if the link passed is a valid link or not, check if the api errors out with status.code > 200
        """
        
        return requests.head(self.payload, allow_redirects = True).status_code
    
    def print_attributes(self):
        print(f"{'payload:':15} {self.payload}")
        print(f"{'status code:':15} {self.status}")
                

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


class KeywordExtractorAgent(AgentManager):    

    def __init__(self, thought, nlp):

        self.manager = AgentManager(thought)
        self.nlp = nlp 
        self.manager.skill = 'Extract Keywords'
        self.ents, self.proper_nouns, self.keywords = self.keyword_extractor()
        self.print_attributes()
    
    def keyword_extractor(self):
        
        """
        We are first extracting all the entities derived from spacy and then appending it to the keyword list
        However this misses some proper nouns in the text that spacy doesn't recognize as an entity (eg: "Pybrain")
        To account for this, we create a list of proper nouns and construct a string of all the extracted entities. 
        We then check whether any proper nouns is in the string, if it is skip to the next proper noun and if not add to the keyword list with NNP tag. 
        We do this because the extracted proper nouns overlap with the extracted entities but not always an exact match. 
        (eg: "Society of Mind" as a single entity, whereas the proper noun extracts Society and Mind as separate nouns.)
        """

        
        
        curr_thought = self.manager.input
        doc = self.nlp(curr_thought.d.description)
        keywords = []
        ents = [(e.text, e.label_) for e in doc.ents]
        proper_nouns = [t.text for t in doc if t.tag_ == 'NNP']
        
        ent_string = " ".join([ent for ent,label in ents])
        
        for (ent,label) in ents:
            keywords.append((ent,label))
            
        for pn in proper_nouns:
            if pn in ent_string:
                pass
            else:
                keywords.append((pn,'NNP')) 
             
        return ents, proper_nouns, keywords
    
       
    def print_attributes(self):
        print(self.manager.skill, end = f'\n{"-"*40}\n')
        print(self.keywords)