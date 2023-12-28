import json

with open('E:/Cromwell/cromwell/cromwell_links2_uk.json' , 'r') as f:
    urls = json.load(f)

temp = []
for url in urls:
    item = {
        'link' : url
    }
    temp.append(item)
with open('final_cromwell_links2_uk.json' , 'w') as g:
    json.dump(temp , g)
