#!/usr/bin/env python
import igraph as G
import json, sys
from os import listdir
import csv
import time
import re

g = [G.Graph(directed=True),G.Graph(directed=True),G.Graph(directed=True)]

files = listdir('tweets')
users=[["user"]]
for file in files:
    #print file
    json_data=open('tweets/' + str(file)).read()
    data = json.loads(json_data)
    #print(data)

    if not (isinstance(data, dict)):
        ## not a dictionary, skip
        pass
    elif 'delete' in data:
        ## a delete element, skip for now.
        pass
    elif 'user' not in data:
        ## bizarre userless edge case
        pass
    else:
        user = data['user']['screen_name']
        if user not in users:
            #print user
            users.append([user])

#print mentions
with open("users.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(users)
