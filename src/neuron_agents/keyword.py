import functools
import spacy 

nlp = spacy.load('en_core_web_lg')

print(type(nlp))

doc = nlp("How to write singleton classes in Python, i.e. classes where only a single instance is allowed to be created.")

print(type(doc))



def write_decorator(func):
    "Writes the output to a file"
    @functools.wraps(func)
    def writer(*args, **kwargs):
        with open("/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/spacy_op.txt", mode='a') as f:
            f.write(f"FUNC: {func.__name__}:\n"+str(func(*args, **kwargs))+"\n"+ "---"*25 +"\n")
    return writer

@write_decorator
def noun_printer(doc):
    return [nc for nc in doc.noun_chunks]

#noun_printer(doc)
#token_printer_no_stop(doc)

@write_decorator
def token_printer_no_stop(doc):
    return [return_one_by_one(t) for t in doc if not t.is_stop]

@write_decorator
def dep_printer(doc):
    return [return_one_by_one(token, token.dep_,token.head.text, token.head.pos_, [child for child in token.children]) for token in doc]

#doc = nlp("A video of Nancy's brain being zapped by Transcranial Mangnetic Simulation")

@write_decorator
def return_one_by_one(*args):
    return args

#noun_printer(doc)
#token_printer_no_stop(doc)
#dep_printer(doc)

doc = nlp("A course by ex-Google and Facebook engineers and also BITs Pilani and Georgia Tech educated, on state of art NLP.")

print("{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^20s}".format("token","ent","dep", "head"," pos"," children"))
print("-"*120,end='\n')
for t in doc:
  print("{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^15s}\t{:^20s}".format(t.text, 
                                                                      str([(ent.label_,t.ent_iob) for ent in doc.ents if ent.text == t.text]), 
                                                                      t.dep_, 
                                                                      t.head.text, 
                                                                      t.head.pos_, 
                                                                      str([child for child in t.children])))
  print("-"*120,end='\n')