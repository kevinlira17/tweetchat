
# STANFORD AVERAGE SENTIMENT VALUE OF CORPUS
# REQUIRES PIP INSTALL STANFORDCORENLP AND 'STANFORD-CORENLP-FULL-2018-02-27'
# (FREE) IN DIRECTORY

# 1.754 for frown without emoji
# 1.657 with frown emoji???
# 2.02 with smile emoji
# 2.136 without smile emoji ???


import os
import json
from stanfordcorenlp import StanfordCoreNLP

f = open("cleanSmile.txt", "r", encoding="utf8")
p = open("smileClassificationWithEmoji.txt", "w", encoding="utf8")

#start it up
dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + '\stanford-corenlp-full-2018-02-27'
nlp = StanfordCoreNLP(path)


totalSentimentValue = 0
nDoneSoFar = 0
for line in f:
    try:
        sentenceSentimentValue = 0
        res = nlp.annotate(line, properties={'annotators': 'sentiment'})
        asjson = json.loads(res)

        for s in asjson['sentences']:
            nDoneSoFar += 1
            sentenceSentimentValue += int(s['sentimentValue'])
        p.write(str(sentenceSentimentValue) + "\t" + line)
        totalSentimentValue += sentenceSentimentValue
            
    except ValueError:
        print("gah oh no")
        
#shut it down
nlp.close()
f.close()
p.close()

print("Number of tweets: " + str(nDoneSoFar))
print("Average sentiment value: " + str(totalSentimentValue / nDoneSoFar))

