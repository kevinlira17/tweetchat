# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:09:45 2018
@author: link9
"""

from nltk import FreqDist
import math
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
training = open("TrainingNegativeNoEmoji.txt", "r", encoding="utf8")
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
        #print(w)
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
    bigrams = ngrams(reviewwords.split(),2)
    trigrams= ngrams(reviewwords.split(),3)
    ### POSITIVE SCORE
    posscore=0
    negscore=0
    for pair in bigrams:
        if pair in affinityPosBGprobs.keys():
            #print(pair)
            posscore+=affinityPosBGprobs[pair]
        if pair in affinityNegBGprobs.keys():
            negscore+=affinityNegBGprobs[pair]
    for trip in trigrams:
        if trip in affinityPosTGprobs.keys():
            #print(trip)
            posscore+=affinityPosTGprobs[trip]
        if trip in affinityNegTGprobs.keys():
            negscore+=affinityNegTGprobs[trip]
    #print(posscore1-negscore1, posscore-negscore)
    #for key in affinityPosTGprobs.keys():
        #posscore+=affinityPosTGprobs[key]
    #for key in affinityPosBGprobs.keys():
        #posscore+=affinityPosBGprobs[key]
    #for key in affinityNegTGprobs.keys():
        #negscore+=affinityNegTGprobs[key]
    #for key in affinityNegBGprobs.keys():
        #negscore+=affinityNegBGprobs[key]
    #for i in range(1, len(reviewwords)):
        #posscore += poswordprobs.get(reviewwords[i], defaultprob)
        #ALSO POSSCORE += affinityPosBGProbs.get((reviewwords[i],reviewwords[i+1]))

    ### CALCULATE NEGATIVE SCORE
    #negscore = negwordprobs.get(reviewwords[0], defaultprob)
    #for i in range(1, len(reviewwords)):
        #negscore += negwordprobs.get(reviewwords[i], defaultprob)
    #print(posscore)
    if (posscore - negscore) >  0:
        return "1"

    return "0"

vals=[]
testing = []
testinglabel = []

nbcorrect = 0
numberLines = 0
testdata = open("TestNegativeNoEmoji.txt", "r", encoding="utf8")
for line in testdata:

    numberLines += 1
    pol = line[0]
    if pol == 0:
        testinglabel.append(0)
    else:
        testinglabel.append(1)
    tweet = line[2:]
    testing.append([str(tweet)])

    if pol == affinity(tweet):
        nbcorrect += 1

testdata.close()

numberTruePositivesForPos = 0
numberFalsePositivesForPos = 0
numberFalseNegativesForPos = 0
numberTruePositivesForNeg = 0
numberFalsePositivesForNeg = 0
numberFalseNegativesForNeg = 0
testdata = open("TestNegativeNoEmoji.txt", "r", encoding="utf8")
numberLines = 0
for line in testdata:

    numberLines += 1
    pol = line[0]
    if pol == "0":
        testinglabel.append(0)
    else:
        testinglabel.append(1)
    tweet = line[2:]
    testing.append([str(tweet)])

    result = affinity(tweet)
    #SAY POSITIVE SENTIMENT IS "POSITIVE"
    #print(result==pol,result)
    if result == pol:
        #MUST BE TRUE POS FOR POS SENTIMENT OR TRUE POS FOR NEG SENTIMENT
        if result == "1":
            numberTruePositivesForPos += 1
        else:
            numberTruePositivesForNeg += 1
    else:
        #WAS MIS-CATEGORIZED
        if result == "1": #AND WAS WRONG
            numberFalsePositivesForPos += 1
            numberFalseNegativesForNeg += 1
        else: # RESULT WAS NEG AND SHOULD HAVE BEEN POS
            numberFalseNegativesForPos += 1
            numberFalsePositivesForNeg += 1

testdata.close()
print(numberFalseNegativesForPos)
#print("Naive Bayes accuracy: ", (nbcorrect/numberLines))
precision = (((numberTruePositivesForPos / (numberTruePositivesForPos + numberFalsePositivesForPos)) + (numberTruePositivesForNeg/(numberTruePositivesForNeg+numberFalsePositivesForNeg)))/2)
print("Averaged Precision of Affinity: ", precision)
recall = (((numberTruePositivesForPos / (numberTruePositivesForPos + numberFalseNegativesForPos)) + (numberTruePositivesForNeg/(numberTruePositivesForNeg+numberFalseNegativesForNeg)))/2)
print("Averaged Recall of Affinity: ", recall)
fscore = (2 * precision * recall)/(precision + recall)
print("Averaged F-Score of Affinity: ", fscore)
