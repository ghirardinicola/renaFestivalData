#!/usr/bin/env python

import json, sys
from os import listdir
import csv
import io
import re
import math
from collections import Counter
import time

stopWords = set()

with open('download/stop-words_italian_1_it.txt', 'rb') as f:
    for word in f.readlines():
        stopWords.update((word[:-2].decode('utf-8'),))

with open('download/stop-words_italian_2_it.txt') as f:
    for word in f.readlines():
        stopWords.update((word[:-2].decode('utf-8'),))


textAll = ["","",""]
files = listdir('tweets')
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
        t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Sat Jun 14 13:30:00 +0000 2014",'%a %b %d %H:%M:%S +0000 %Y'))
        t2 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Sat Jun 14 18:30:15 +0000 2014",'%a %b %d %H:%M:%S +0000 %Y'))
        t3 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Sun Jun 15 05:30:15 +0000 2014",'%a %b %d %H:%M:%S +0000 %Y'))
        if (ts<t1):
            when=1
        elif (ts<t2):
            when=2
        elif (ts<t3):
            when=3
        #print when
        text=data['text']
        #escludo i retwreet  sopratutto per l'orario
        if not re.match("^RT*", text):
            textAll[when-1] += " "
            textAll[when-1] += format(text)


textAll2=textAll
cntAll = Counter()

for when, textAll in enumerate(textAll2):
#for when,textAll in textAll2:
    cnt = Counter()
    for word in textAll.split():
        word=word.lower()
        if word[0]=='#':
            word=word[1:]
        if word not in stopWords:
            if not re.match("@.*", word):
                if not re.match("^http.*", word):
                    if (len(word)  > 3):
                        word = re.sub('[!@#$,.:"?]', '', word)
                        x = unicode("renafestival")
                        if unicode(word) != x:
                            cnt[word] += 1  
                            cntAll[word] += 1  

    wordcsv=[["term","freq"]]
    for word2, count in cnt.most_common(75):
        wordcsv.append([word2.encode('utf-8'),str(count).encode('utf-8')])

    with open("word"+str(when+1)+".csv", 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(wordcsv)  

wordcsvAll=[["term","freq"]]

for word2, count in cntAll.most_common(75):
    wordcsvAll.append([word2.encode('utf-8'),str(count).encode('utf-8')])

with open("word.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(wordcsvAll)   