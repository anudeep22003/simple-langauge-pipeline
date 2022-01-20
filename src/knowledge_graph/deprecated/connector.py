from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship

g = Graph("neo4j+s://8219a15b.databases.neo4j.io:7687", auth = ("neo4j", "SHHcaUZYNPF-qWoyOrahHksjOelYBFASgdqjrRd1Ju8"))

tx = g.begin()

# delete all nodes to start afresh 
g.delete_all()

m = Node("Greeting", message = "this is a modifications")
b = Node("Greeting", message = "got this working pretty quick")
c = Node("Followup", follow_message = "Want to go grab dinner")
ncl = []
ncl.append(Relationship(b,'CAME_BEFORE',m, weight= .9887, hoecount = 4))
ncl.append(Relationship(c,'CAME_hence',b))
ncl.append(Relationship(c,'CAME_AFTER',m))

for nc in ncl:
    tx.create(nc)

g.commit(tx)

#print(g.run('MATCH (g: Greeting) RETURN g.message'))



