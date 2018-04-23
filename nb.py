# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:09:45 2018

@author: link9
"""

from nltk import FreqDist
import glob
from nltk.corpus import stopwords
import math
import re

###########################
## READ IN TRAINING DATA ##
###########################


## Read in all positive reviews
## We create a set of unique words for each review. No duplicates.
## We then add that set of words as a list to the master list of positive words.
poswords = []
negwords = []
training = open("allClassifiedTrainingNoEmoji.txt", "r", encoding="utf8")
for line in training:
    words = line.rstrip().split()
    sen = line[0:3]
    tweet = line[4:]
    if sen == 'pos':
        poswords.extend(list(set([w for w in words])))
    else:
        negwords.extend(list(set([w for w in words])))

training.close()

###########################################################
## GET NAIVE BAYES PROBABILITIES FOR POS AND NEG CLASSES ##
###########################################################


   #########################################################
   ################# YOUR CODE BEGINS HERE #################
   #########################################################


## GOAL: Populate these two dicts, where each
##      key = word from the pos or neg word list
##      value = NB probability for that word in that class
## You will refer to these dicts in your function
## definition, below, for naive_bayes()
poswordprobs = {}
negwordprobs = {}

## You might need to know the number of tokens and types
## in each of the two classes.
postok = len(poswords)
negtok = len(negwords)
postype = len(set(poswords))
negtype = len(set(negwords))

## And you might need a list of all the words in both sets.
allwords = list(set(negwords)) + list(set(poswords))


## Start by creating FreqDists for poswords and for negwords below
posFreqDist = FreqDist(poswords)
negFreqDist = FreqDist(negwords)

## Loop through your poswords FreqDist, and calculate the
## probability of each word in the positive class, like this:
## P(word|pos) = count(word) / postok
## Store the results in poswordprobs
## USE LOGS!!!
for posW in posFreqDist:
    probWIsPos = math.log(posFreqDist[posW] / postok)
    poswordprobs[posW] = probWIsPos



## Now, loop through your negwords FreqDist, and calculate the
## probability of each word in the negative class, like this:
## P(word|neg) = count(neg) / postok
## Store the results in negwordprobs
## USE LOGS!!!
for negW in negFreqDist:
    probWIsNeg = math.log(negFreqDist[negW] / negtok)
    negwordprobs[negW] = probWIsNeg

    #########################################################
    ################# YOUR CODE ENDS HERE ###################
    #########################################################



######################################
### FUNCTIONS TO PREDICT SENTIMENT ###
######################################



## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
def naive_bayes(reviewwords):

    defaultprob = math.log(0.0000000000001)
    
    ### POSITIVE SCORE
    posscore = poswordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        posscore += poswordprobs.get(reviewwords[i], defaultprob)

    ### CALCULATE NEGATIVE SCORE
    negscore = negwordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        negscore += negwordprobs.get(reviewwords[i], defaultprob)

    if (posscore - negscore) >  0:
        return "pos"

    return "neg"


#################################################
### PREDICT THE SENTIMENT OF THE TEST REVIEWS ###
#################################################

nbcorrect = 0
numberLines = 0
testdata = open("classifiedTestData.txt", "r", encoding="utf8")
for line in testdata:

    numberLines += 1
    pol = line[0:3]
    tweet = line[4:]

    if pol == naive_bayes(tweet):
        nbcorrect += 1

testdata.close()

print("Naive Bayes accuracy: ", (nbcorrect/numberLines))



################################################################

# CODE OUTLINE FOR CONTINUING ANALYSIS WITH OTHER CLASSIFIERS
## Get the 1000 most frequent words
## These will be your features
wfreq = FreqDist(allwords)
top1000 = wfreq.most_common(1500)

training = []
traininglabel = []

# Take each review, and create a feature vector.
# For each word in the top1000, if that review contains
# that word, set its vector value to 1; otherwise 0.

for p in poswords:
    vec = []
    for t in top1000:
        if t[0] in p:
            vec.append(1)
        else:
            vec.append(0)
    training.append(vec)
    traininglabel.append(1)

for n in negwords:
    vec = []
    for t in top1000:
        if t[0] in n:
            vec.append(1)
        else:
            vec.append(0)
    training.append(vec)
    traininglabel.append(0)
# now read in the testing data
# for each testing example, create a vector
# of bninary features just as you did for the training data
testing = []
testinglabel = []

testdata = glob.glob("test/*")
for filename in testdata:

    rw = []
    f = open(filename)
    filepolarity = re.sub(r"^.*?(pos|neg)-.*?$", r"\1", filename)

    for line in f:
        words = line.rstrip().split()
        rw.extend(words)
    f.close()

    vec = []
    for t in top1000:
        if t[0] in rw:
            vec.append(1)
        else:
            vec.append(0)
    testing.append(vec)

    if filepolarity == "neg":
        testinglabel.append(0)
    else:
        testinglabel.append(1)
        
print(len(testing))
### NEURAL NET CLASSIFIER                                                                                       
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 3), random_state=1)
clf.fit(training, traininglabel)
predicted = clf.predict(testing)
print("Accruracy of Multi-Layer Perceptron")
print(metrics.classification_report(testinglabel, predicted))

## Classifier 1
clf2 = KNeighborsClassifier(n_neighbors=60)
clf2.fit(training, traininglabel)
predicted = clf2.predict(testing)
print("Accruracy of K-Nearest Neighbors")
print(metrics.classification_report(testinglabel, predicted))


## Classifier 2
clf3 = LinearSVC()
clf3.fit(training, traininglabel)
predicted = clf3.predict(testing)
print("Accruracy of Linear SVC")
print(metrics.classification_report(testinglabel, predicted))
