
# STANFORD AVERAGE SENTIMENT VALUE OF CORPUS
# REQUIRES PIP INSTALL STANFORDCORENLP AND 'STANFORD-CORENLP-FULL-2018-02-27'
# (FREE) IN DIRECTORY

import os
import json
from stanfordcorenlp import StanfordCoreNLP

f = open("cleanFrown.txt", "r", encoding="utf8")

#start it up
dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + '\stanford-corenlp-full-2018-02-27'
nlp = StanfordCoreNLP(path)


totalSentimentValue = 0
nDoneSoFar = 0
for line in f:
    try:
        res = nlp.annotate(line, properties={'annotators': 'sentiment'})
        print(res)
        asjson = json.loads(res)

        for s in asjson['sentences']:
            nDoneSoFar += 1
            totalSentimentValue += int(s['sentimentValue'])
            
    except ValueError:
        print("gah oh no")
        
#shut it down
nlp.close()
f.close()

print("Average sentiment value: " + str(totalSentimentValue / nDoneSoFar))
