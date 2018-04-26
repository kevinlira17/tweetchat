
from nltk import FreqDist
import math
import nltk

def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append((input_list[i], input_list[i+1]))
  return bigram_list
###########################
## READ IN TRAINING DATA ##
###########################


## Read in all positive reviews
## We create a set of unique words for each review. No duplicates.
## We then add that set of words as a list to the master list of positive words.
poswords = []
negwords = []
posbigrams = []
negbigrams = []
training = open("allClassifiedTraining.txt", "r", encoding="utf8")
for line in training:
    #words = line.rstrip().split()
    sen = line[0:3]
    tweet = line[4:].rstrip().split()
    if sen == 'pos':
        poswords.extend(list(set([w for w in tweet])))
        #print(find_bigrams(tweet))
        #posbigrams.extend(list(set([ngrams(tweet,2) in tweet])))
        posbigrams.extend(find_bigrams(tweet))
    else:
        negwords.extend(list(set([w for w in tweet])))
        #negbigrams.extend(list(set([ngrams(tweet,2) in tweet])))
        negbigrams.extend(find_bigrams(tweet))
training.close()



poswordprobs = {}
negwordprobs = {}

postok = len(poswords)
negtok = len(negwords)
postype = len(set(poswords))
negtype = len(set(negwords))

allwords = list(set(negwords)) + list(set(poswords))


posFreqDist = FreqDist(poswords)
negFreqDist = FreqDist(negwords)

posBigramFDist = nltk.FreqDist(posbigrams)
negBigramFDist = nltk.FreqDist(negbigrams)
posBigramFDist = dict(posBigramFDist)
negBigramFDist = dict(negBigramFDist)


affinityPosBGProbs = {}
affinityNegBGProbs = {}


## Loop through your poswords FreqDist, and calculate the
## probability of each word in the positive class, like this:
## P(word|pos) = count(word) / postok
## Store the results in poswordprobs
## USE LOGS!!!
for posW in posFreqDist:
    probWIsPos = math.log(posFreqDist[posW] / postok)
    poswordprobs[posW] = probWIsPos

for negW in negFreqDist:
    probWIsNeg = math.log(negFreqDist[negW] / negtok)
    negwordprobs[negW] = probWIsNeg
  

for key, value in posBigramFDist.items():
    w1 = key[0]
    w2 = key[1]
    count1 = posFreqDist[w1]
    count2 = posFreqDist[w2]
    
    #WANT AFFINITY
    minFreq = min(posFreqDist[w1], posFreqDist[w2])
    affinity = value/minFreq
    #PMI = math.log2(N*(colloq[1]/(count1 * count2)))
    affinityPosBGProbs.update({key: affinity})
    
#REPEAT FOR negBG
    
for key, value in negBigramFDist.items():
    w1 = key[0]
    w2 = key[1]
    count1 = negFreqDist[w1]
    count2 = negFreqDist[w2]
    
    #WANT AFFINITY
    minFreq = min(negFreqDist[w1], negFreqDist[w2])
    affinity = value/minFreq
    #PMI = math.log2(N*(colloq[1]/(count1 * count2)))
    affinityPosBGProbs.update({key: affinity})

######################################
### FUNCTIONS TO PREDICT SENTIMENT ###
######################################



## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
    
def affinity(reviewwords):

    defaultprob = math.log(0.0000000000001)
    
    ### POSITIVE SCORE
    posscore = 0
    #posscore = poswordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)-1):
        # NOT SURE IF NEED BELOW LINE
        #posscore += poswordprobs.get(reviewwords[i], defaultprob)
        posscore += affinityPosBGProbs.get((reviewwords[i],reviewwords[i+1]), defaultprob)

    ### CALCULATE NEGATIVE SCORE
    negscore = 0
    #negscore = negwordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)-1):
        # NOT SURE IF NEED BELOW LINE
        #negscore += negwordprobs.get(reviewwords[i], defaultprob)
        negscore += affinityNegBGProbs.get((reviewwords[i],reviewwords[i+1]), defaultprob)

    if (posscore - negscore) >  0:
        return "pos"

    return "neg"


testing = []
testinglabel = []

nbcorrect = 0
numberLines = 0
testdata = open("classifiedTestData.txt", "r", encoding="utf8")
for line in testdata:

    numberLines += 1
    pol = line[0:3]
    if pol == "neg":
        testinglabel.append(0)
    else:
        testinglabel.append(1)
    tweet = line[4:]
    testing.append([str(tweet)])

    if pol == affinity(tweet):
        nbcorrect += 1

testdata.close()
print("Naive Bayes accuracy: ", (nbcorrect/numberLines))

