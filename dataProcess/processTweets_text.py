#!/usr/bin/env python

import json, sys
from os import listdir
import csv
import io
import re
import math
from collections import Counter

stopWords = set()

with open('download/stop-words_italian_1_it.txt', 'rb') as f:
    for word in f.readlines():
        stopWords.update((word[:-2].decode('utf-8'),))

with open('download/stop-words_italian_2_it.txt') as f:
    for word in f.readlines():
        stopWords.update((word[:-2].decode('utf-8'),))


textAll = ""
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
        text=data['text']
        #print text
        textAll += " "
        textAll += format(text)



#print textAll
file = io.open('texts.txt', 'w', encoding='utf8')
file.write(format(textAll))


# wordcount={}
# for word in textAll.split():
#     if word not in wordcount:
#         wordcount[word] = 1
#     else:
#         wordcount[word] += 1
# for k,v in wordcount.items():
#     print k, v

#common_word_dic=['e','il','con','un','a','per','la','le','in','una','delle','ci','sono','del','ma','che','RT','non','di','Le','si','della','al','']

cnt = Counter()
for word in textAll.split():
    word=word.lower()
    if word[0]=='#':
        word=word[1:]
    if word not in stopWords:
        if not re.match("^@.*", word):
            if not re.match("^http.*", word):
                if (len(word)  > 4):
                    cnt[word] += 1

for word, count in cnt.most_common(200):
    print '%s: %7d' % (word, count)

wordcsv=[["term","freq"]]
for word, count in cnt.most_common(100):
    #wordcsv.append([word.encode('utf-8'),str(int(math.log10(count)*100.)).encode('utf-8')])
    wordcsv.append([word.encode('utf-8'),str(count).encode('utf-8')])

with open("word.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(wordcsv)    
