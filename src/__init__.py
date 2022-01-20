import random
import requests
import spacy

nlp = spacy.load('en_core_web_sm')

import nltk
import pandas as pd
import numpy as np
import math

from spacy import displacy
from spacy.symbols import nsubj, VERB, PROPN


from classes import *


t = ThoughtBlock('https://www.founderlibrary.com/', """Found from Lenny Rachitsky's website, looks like a great set of reads for founders right from fundraising, Investor relations, to Product and Hiring.""")

t.print_attributes()

k = KeywordExtractorAgent(thought=t, nlp= nlp)