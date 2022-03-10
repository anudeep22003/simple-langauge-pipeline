from pprint import pprint
from urllib.parse import urlparse
import re, json

url_pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))')
res = urlparse("https://www.google.com/search?q=link+query+url+parser+python&sxsrf=APq-WBuEHDe9kOaXbXjGHQvXwnu7DMhgJg%3A1644822296403&ei=GP8JYvj-F7rWz7sP4qSVuAo&ved=0ahUKEwj46sfF0P71AhU663MBHWJSBacQ4dUDCA8&uact=5&oq=link+query+url+parser+python&gs_lcp=Cgdnd3Mtd2l6EAMyCAghEBYQHRAeOgcIABBHELADOgQIIRAKSgQIQRgASgQIRhgAULsEWLMVYL8XaAFwAXgAgAGpAYgB4QaSAQMwLjeYAQCgAQHIAQjAAQE&sclient=gws-wiz", allow_fragments=True)

d = {}

with open(file='/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/cypher_to_sql_message.txt',mode='r') as f:
    for line in f.readlines():
        for match in re.findall(url_pattern,line):
            try:
                res = urlparse(match[0],allow_fragments=True)
            except Exception as e:
                print(f"Error caught: {type(e)}, args: {e.args} ")
            # print(f"type: {type(res.query)}\t{res.query}",end='\n')
            # print(f"type: {type(res.path)}\t{res.path}",end='\n')
            # print("---"*40,end='\n')
            minimum_url = "".join((res.netloc,res.path))
            try: 
                d[res.netloc]
            except:
                d[res.netloc]=[(res.path,res.query)]
            else:
                d[res.netloc].append((res.path,res.query))

with open(file="/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/misc-code/data_output/url_json.txt",mode='a') as f:
    json.dump(obj=d,fp=f)


            


# l = [res.path,res.query,res.fragment, res.netloc]
# print("---"*40,end='\n\n')
# for li in l:
#     print(li, end='\n\n')