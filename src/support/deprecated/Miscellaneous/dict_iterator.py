d = {
    'Anudeep': 'M',
    'Vinny': 'F',
    "Amma": 'M',
    'Nana': 'M'
}
for i in d.values():
    print(i)


l = []
l.append(d)
l.append(d)
print(l)



def foo(a,b):
    baa(b)
    return a+b

def baa(b):
    return 2*b

print(foo(5,baa(4)))