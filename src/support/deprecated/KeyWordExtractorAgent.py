
class KeywordExtractorAgent(AgentManager):
    def __init__(self, thought):
        self.manager = AgentManager(thought)
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
        doc = nlp(curr_thought.d.description)
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