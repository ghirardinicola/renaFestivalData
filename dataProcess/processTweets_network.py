#!/usr/bin/env python
import igraph as G
import json, sys
from os import listdir
import csv

g = G.Graph(directed=True)

files = listdir('tweets')
mentions=[["source","target"]]
for file in files:
    print file
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
        if 'entities' in data and len(data['entities']['user_mentions']) > 0:
            user = data['user']
            user_mentions = data['entities']['user_mentions']

            for u2 in user_mentions:
                print "\t".join([
                    user['id_str'],
                    u2['id_str']
                    ])
                mention=[str(user['screen_name']),str(u2['screen_name'])]
                ufrom = user['screen_name']
                uto = u2['screen_name']
                try:
                    g.vs.find(name=ufrom)
                except:
                    g.add_vertex(name=ufrom)

                try:
                    g.vs.find(name=uto)
                except:
                    g.add_vertex(name=uto)

                u=g.vs.find(name=ufrom)
                v=g.vs.find(name=uto)

                g.add_edge(u,v,weight=1.0)
                mentions.append(mention)

from IPython import embed; embed()

#g.vs.find(name='ProgettoRENA').delete()

g.simplify(combine_edges='sum')

with open('edges.csv','w+') as f:
    for e in g.es:
        for i in range(int(e['weight'])):
            f.write(('%s,%s\n'%(g.vs[e.source]['name'],g.vs[e.target]['name'])))


print mentions
with open("mentions.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(mentions)
