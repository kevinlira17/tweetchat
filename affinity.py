# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:09:45 2018
@author: link9
"""

from nltk import FreqDist
import math
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np
import nltk
from nltk.util import ngrams


###########################
## READ IN TRAINING DATA ##
###########################


## Read in all positive reviews
## We create a set of unique words for each review. No duplicates.
## We then add that set of words as a list to the master list of positive words.
poswords = []
negwords = []
training = open("Training.txt", "r", encoding="utf8")
for line in training:
    words = line.rstrip().split()
    sen = line[0]
    tweet = line[2:]
    if sen == '1':
        poswords.extend(words[1:])
    else:
        negwords.extend(words[1:])

training.close()


poswordprobs = {}
negwordprobs = {}

affinityprobs = {}

postok = len(poswords)
negtok = len(negwords)
postype = len(set(poswords))
negtype = len(set(negwords))


allwords = list(set(negwords)) + list(set(poswords))

posFreqDist = FreqDist(poswords)
negFreqDist = FreqDist(negwords)

posBigrams = ngrams(poswords,2)
posBigramFDist = nltk.FreqDist(posBigrams)
posBigramList=list(posBigramFDist.keys())
negBigrams = ngrams(negwords,2)
negBigramFDist = nltk.FreqDist(negBigrams)
negBigramList=list(negBigramFDist.keys())

posTrigrams = ngrams(poswords,3)
posTrigramFDist = nltk.FreqDist(posTrigrams)
posTrigramList=list(posTrigramFDist.keys())
negTrigrams = ngrams(negwords,3)
negTrigramFDist = nltk.FreqDist(negTrigrams)
negTrigramList=list(negTrigramFDist.keys())


affinityPosBGprobs = {}
affinityNegBGprobs = {}

affinityPosTGprobs = {}
affinityNegTGprobs = {}


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
    
#for posBG in posBigramFDist:
    #w1 = posBG[0]
    #w2 = posBG[1]
    #count1 = poswords[w1]
    #count2 = poswords[w2]
    
    #WANT AFFINITY
    #PMI = math.log2(N*(colloq[1]/(count1 * count2)))
for phrase in posBigramList:
    pFreq=posBigramFDist[phrase]
    wFreq=float("Inf")
    for w in phrase:
        if phrase.count(w)<wFreq:
            wFreq=phrase.count(w)
    affinityPosBGprobs[phrase]=pFreq/wFreq
    #posAllNGrams.append((posBG[0], affinity))
for phrase in negBigramList:
    pFreq=negBigramFDist[phrase]
    wFreq=float("Inf")
    for w in phrase:
        if phrase.count(w)<wFreq:
            wFreq=phrase.count(w)
    affinityNegBGprobs[phrase]=pFreq/wFreq
    
for phrase in posTrigramList:
    pFreq=posTrigramFDist[phrase]
    wFreq=float("Inf")
    for w in phrase:
        if phrase.count(w)<wFreq:
            wFreq=phrase.count(w)
    affinityPosTGprobs[phrase]=pFreq/wFreq
    #posAllNGrams.append((posBG[0], affinity))
for phrase in negTrigramList:
    pFreq=negTrigramFDist[phrase]
    wFreq=float("Inf")
    for w in phrase:
        if phrase.count(w)<wFreq:
            wFreq=phrase.count(w)
    affinityNegTGprobs[phrase]=pFreq/wFreq
    
#REPEAT FOR negBG

######################################
### FUNCTIONS TO PREDICT SENTIMENT ###
######################################



## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
    
#REWORK
def affinity(reviewwords):

    #defaultprob = math.log(0.0000000000001)
    
    ### POSITIVE SCORE
    posscore=0
    negscore=0
    for key in affinityPosTGprobs.keys():
        posscore+=affinityPosTGprobs[key]
    for key in affinityPosBGprobs.keys():
        posscore+=affinityPosBGprobs[key]
    for key in affinityNegTGprobs.keys():
        negscore+=affinityNegTGprobs[key]
    for key in affinityNegBGprobs.keys():
        negscore+=affinityNegBGprobs[key]
    #for i in range(1, len(reviewwords)):
        #posscore += poswordprobs.get(reviewwords[i], defaultprob)
        #ALSO POSSCORE += affinityPosBGProbs.get((reviewwords[i],reviewwords[i+1]))

    ### CALCULATE NEGATIVE SCORE
    #negscore = negwordprobs.get(reviewwords[0], defaultprob)
    #for i in range(1, len(reviewwords)):
        #negscore += negwordprobs.get(reviewwords[i], defaultprob)

    if (posscore - negscore) >  0:
        return "pos"

    return "neg"

vals=[]
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

