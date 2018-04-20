
import re
import nltk
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.extend([".", ",", ";", ":", "“", "”", "'", "?", "!", "``", "''", "...", "-", "--", "’", "(", ")", "I", "It", "The", "And", "i", "n't", "'ve", "'d", "'s", "@", "#", "_", "__"])

f = open("smileTweetsRaw.txt", "r", encoding="utf8")

tweets = ''
for line in f:
    if len(line) > 3:
        # add |([^0-9A-Za-z \t]) to get no emoji
        line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(_[0-9A-Za-z_]+)|(#[0-9A-Za-z]+)"," ",line).split())
        linetokens = nltk.word_tokenize(line)
        noStopwords = [token for token in linetokens if token not in stoplist]
        noStopwordsString = ' '.join(noStopwords)
        tweets += (noStopwordsString + "\n")
f.close()

p = open("cleanSmile.txt", "w", encoding="utf8")
p.write(tweets)
p.close()
