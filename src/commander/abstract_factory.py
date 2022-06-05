##### Python imports #####
from abc import ABC, ABCMeta, abstractmethod
from subprocess import call
import sys, os

##### Manual imports #####
sys.path.append(os.path.join(os.getcwd(),'src','interfacers'))
from neo4j_interfacer import Neo4jInterfacer


class Command(metaclass = ABCMeta):
    
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'orchestrate') and 
                callable(subclass.orchestrate) or 
                NotImplemented)
    
    @abstractmethod
    def orchestrate():
        ...


class AbstractNeoInterface(ABC):
    
    neo: Neo4jInterfacer = Neo4jInterfacer()
    
    @abstractmethod
    def query_construct():
        ...
        
    @abstractmethod
    def query_execute(neo):
        ...
    
    
class CommandHandler(metaclass = ABCMeta):
    
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'orchestrate') and 
                callable(subclass.orchestrate) and 
                hasattr(subclass, "choose_your_adventure") and 
                callable(subclass.choose_your_adventure) or 
                NotImplemented)
    
    def orchestrate(self,command: Command):
        ...
    
    def choose_your_adventure(self):
        ...