# def cube(n):
#     return n**3
# 
# l = list(range(20))
# new_l = map(cube, l)
# print(l, list(new_l))
# 
# def some_func(*args):
#     return some_func.__name__, args, type(args)
# 
# print(some_func(3,'k', ['a','n']))
# 
# 
# class Some:
#     var = "global"
# 
#     def __init__(self) -> None:
#         print(Some.var)
# 
# s = Some()
# 
# d = {'hello': 'world'}
# 
# if 'hellod' not in d.keys():
#     print('caught')
# 
# #print(d['hellod'])
# 
# l = ['children','something']
# 
# print('children' in l)
# 
# 
# a = 'my cypher query'
# print(a)
# a = '<ADD MY PIECE> '*5 + '\n' + a
# print(a)


# somedict = {'name': 'Anudeep', 'age': 32, 'designation':'builder' }
# print(somedict)
# print(somedict.values())
# #print(list(somedict.keys()))


import requests
from pprint import pprint as pp

response = requests.head("https://www.slush.org/events/resource-bank/builders-studio/")

pp(dict(response.headers))