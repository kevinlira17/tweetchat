
from nltk import FreqDist
import math
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np


###########################
## READ IN TRAINING DATA ##
###########################


## Read in all positive reviews
## We create a set of unique words for each review. No duplicates.
## We then add that set of words as a list to the master list of positive words.
poswords = []
negwords = []
training = open("TRAINING_NEGATIVE_NO_EMOJI.txt", "r", encoding="utf8")
for line in training:
    sen = line[0]
    tweet = line[2:].rstrip().split()
    if sen == '1':
        poswords.extend(list(set([w for w in tweet])))
    else:
        negwords.extend(list(set([w for w in tweet])))

training.close()

###########################################################
## GET NAIVE BAYES PROBABILITIES FOR POS AND NEG CLASSES ##
###########################################################

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

for negW in negFreqDist:
    probWIsNeg = math.log(negFreqDist[negW] / negtok)
    negwordprobs[negW] = probWIsNeg


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
        return "1"

    return "0"


testing = []
testinglabel = []

#nbcorrect = 0
numberTruePositivesForPos = 0
numberFalsePositivesForPos = 0
numberFalseNegativesForPos = 0
numberTruePositivesForNeg = 0
numberFalsePositivesForNeg = 0
numberFalseNegativesForNeg = 0
numberLines = 0
testdata = open("TEST_NEGATIVE_NO_EMOJI.txt", "r", encoding="utf8")
for line in testdata:

    numberLines += 1
    pol = line[0]
    if pol == "0":
        testinglabel.append(0)
    else:
        testinglabel.append(1)
    tweet = line[2:]
    testing.append([str(tweet)])

    result = naive_bayes(tweet)
    #SAY POSITIVE SENTIMENT IS "POSITIVE"
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
#print("Naive Bayes accuracy: ", (nbcorrect/numberLines))
precision = ((numberTruePositivesForPos / (numberTruePositivesForPos + numberFalsePositivesForPos)) + (numberTruePositivesForNeg/(numberTruePositivesForNeg+numberFalsePositivesForNeg)))/2
print("Averaged Precision of NB: ", precision)
recall = ((numberTruePositivesForPos / (numberTruePositivesForPos + numberFalseNegativesForPos)) + (numberTruePositivesForNeg/(numberTruePositivesForNeg+numberFalseNegativesForNeg)))/2
print("Averaged Recall of NB: ", recall)
fscore = (2 * precision * recall)/(precision + recall)
print("Averaged F-Score of NB: ", fscore)



################################################################

# CODE OUTLINE FOR CONTINUING ANALYSIS WITH OTHER CLASSIFIERS
## Get the 1500 most frequent words
## These will be your features
wfreq = FreqDist(allwords)
top1500 = wfreq.most_common(1500)

training = []
traininglabel = []

# Take each review, and create a feature vector.
# For each word in the top1500, if that review contains
# that word, set its vector value to 1; otherwise 0.

for p in poswords:
    vec = []
    for t in top1500:
        if t[0] in p:
            vec.append(1)
        else:
            vec.append(0)
    training.append(vec)
    traininglabel.append(1)

for n in negwords:
    vec = []
    for t in top1500:
        if t[0] in n:
            vec.append(1)
        else:
            vec.append(0)
    training.append(vec)
    traininglabel.append(0)
# now read in the testing data
# for each testing example, create a vector
# of bninary features just as you did for the training data

realTesting = []


correspondingIndex = 0
for tweet in testing:
    rw = tweet[0].split()

    vec = []
    for t in top1500:
        if t[0] in rw:
            vec.append(1)
        else:
            vec.append(0)
    realTesting.append(vec)
    correspondingIndex += 1

testinglabel2 = np.array(testinglabel)
realTesting2 = np.array(realTesting)



### NEURAL NET CLASSIFIER                                                                                       
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 3), random_state=1)
clf.fit(training, traininglabel)
predicted = clf.predict(realTesting)
print("Accruracy of Multi-Layer Perceptron")
print(metrics.classification_report(testinglabel, predicted))

## Classifier 1
clf2 = KNeighborsClassifier(n_neighbors=20)
clf2.fit(training, traininglabel)
predicted = clf2.predict(realTesting)
print("Accruracy of K-Nearest Neighbors")
print(metrics.classification_report(testinglabel, predicted))

## Classifier 2
clf3 = LinearSVC()
clf3.fit(training, traininglabel)
predicted = clf3.predict(realTesting)
print("Accruracy of Linear SVC")
print(metrics.classification_report(testinglabel, predicted))
