#!/usr/bin/env python
import igraph as G
import json, sys
from os import listdir
import csv
import time
import re

g = [G.Graph(directed=True),G.Graph(directed=True),G.Graph(directed=True)]

files = listdir('tweets')
mentions=[["source","target"]]
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
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Sat Jun 14 13:00:00 +0000 2014",'%a %b %d %H:%M:%S +0000 %Y'))
        t2 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Sat Jun 14 19:30:15 +0000 2014",'%a %b %d %H:%M:%S +0000 %Y'))
        if (ts<t1):
            when=0
        elif (ts<t2):
            when=1
        else:
            when=2
        #print when
        text=data['text']
        if not re.match("^RT*", text):
            if 'entities' in data and len(data['entities']['user_mentions']) > 0:
                user = data['user']
                user_mentions = data['entities']['user_mentions']
               

                for u2 in user_mentions:
                    #    print "\t".join([
                    #    user['id_str'],
                    #    u2['id_str']
                    #    ])
                    mention=[str(user['screen_name']),str(u2['screen_name'])]
                    ufrom = user['screen_name']
                    uto = u2['screen_name']
                    try:
                        g[when].vs.find(name=ufrom)
                    except:
                        g[when].add_vertex(name=ufrom)

                    try:
                        g[when].vs.find(name=uto)
                    except:
                        g[when].add_vertex(name=uto)

                    u=g[when].vs.find(name=ufrom)
                    v=g[when].vs.find(name=uto)

                    g[when].add_edge(u,v,weight=1.0)
                    if unicode(user['screen_name']) == unicode("Tukulti_Ninurta"):
                        print mention
                        print when
                    mentions.append(mention)

#from IPython import embed; embed()

#g.vs.find(name='ProgettoRENA').delete()
for when,gn in enumerate(g):
    gn.simplify(combine_edges='sum')

    with open('edges_'+str(when)+'.csv','w+') as f:
        f.write("source,target\n")
        for e in gn.es:
            for i in range(int(e['weight'])):
                f.write(('%s,%s\n'%(gn.vs[e.source]['name'],gn.vs[e.target]['name'])))


#print mentions
with open("mentions.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(mentions)
