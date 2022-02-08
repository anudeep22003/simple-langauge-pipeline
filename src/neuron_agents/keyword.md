# Approach to buuilding the keyword neuron

## Outline
- [x] Extract language data from sql --> use sql class to write and run the extract clause 
- For each message / row 
  - run through a **keyword_extractor**
  - store the keywords in a dictionary
    - use a try except block, `except KeyError: list.append`
    - (use a class to store the dict and keep track of the kv `keyword, value: tuple(index, position, POS)` pairs)
- write the key value pairs into a file

### SQL Interface:
Ensure the system works for a single sql row (limit to 1)
- [x] `Select uri from message_index LIMIT 10`
- [x] go through each row and print the uri


### Keyword Extractor
- import spacy 
- load a language model by using `spacy.load("en_core_web_sm")` which returns a `language` object
- the `language` object takes either a `doc` or a `str` object and tokenizes it (you can include and not skip different things)



Spacy Architecture

![image](https://spacy.io/architecture-415624fc7d149ec03f2736c4aa8b8f3c.svg)















### Simple Approach 

**Input**
- user input text 
- metadata 
  - `link-title` text
  - other metadata ---> is there any other metadata (see `oembed meta tagged` data)
- html page input (longer text)

**Output**
- keyword pairs (keyword, POS) --> make the POS an `edge attribute`
```
# to keep things simple, I am considering a single keyword only for now

merge (k:Keyword {
  kw: "quantum",
  # keyword_variations: ['quantum', 'quanta', 'quant']
})

with k

merge (m:Message)-[r:keyword_relation {
  pos: 'NNP'
  word: 'quanta'
  number_of_occurences: 3

}]-(k)
```

**Processing**
- create a spacy pipeline <!-- !check huggingface -->
  - pipeline functions --> tokenize --> tag --> sentence structure 
  - isolate words that are compound words >(figure out a way to parse the tree and pair the compound words into a single keyword)
- keywords schema:
  - all keyword will be single words
    - how do we deal with lemmas
        
```
(thought)-[:Relationship {
    pos: 'NN/VBP/....'
    de-lemma: 'liked'   # if lemmatized form is 'like'
    word_position: 5    # position in sequence of words 
}]->(keyword)

```
  - compound keywords will be constructed as a composition of single keywords