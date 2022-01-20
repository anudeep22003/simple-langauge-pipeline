import json

with open(file='src/knowledge_graph/sample.json') as f:
    converted = json.load(fp = f)
    for item in converted:
        print(type(item))
        print(item.keys())
        print(item['id'])
    pass