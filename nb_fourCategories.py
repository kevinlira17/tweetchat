
from nltk import FreqDist
import glob
from nltk.corpus import stopwords
import math
import re

###########################
## READ IN TRAINING DATA ##
###########################

smileWords = []
frownWords = []
tDWords = []
tUWords = []
training = open("allClassifiedTrainingNoEmoji.txt", "r", encoding="utf8")
for line in training:
    words = line.rstrip().split()
    sen = line[0:2]
    tweet = line[4:]
    if sen == 'sm':
        print("yes")
        smileWords.extend(list(set([w for w in words])))
    elif sen == 'fr':
        frownWords.extend(list(set([w for w in words])))
    elif sen == 'tU':
        tDWords.extend(list(set([w for w in words])))
    elif sen == 'tD':
        tUWords.extend(list(set([w for w in words])))

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
smilewordprobs = {}
frownwordprobs = {}
tUwordprobs = {}
tDwordprobs = {}

## You might need to know the number of tokens and types
## in each of the two classes.
smiletok = len(smileWords)
frowntok = len(frownWords)
tUtok = len(tUWords)
tDtok = len(tDWords)
smiletype = len(set(smileWords))
frowntype = len(set(frownWords))
tUtype = len(set(tUWords))
tDtype = len(set(tDWords))

## And you might need a list of all the words in both sets.
allwords = list(set(smileWords)) + list(set(frownWords)) + list(set(tUWords)) + list(set(tDWords))


## Start by creating FreqDists for poswords and for negwords below
smileFreqDist = FreqDist(smileWords)
frownFreqDist = FreqDist(frownWords)
tUFreqDist = FreqDist(tUWords)
tDFreqDist = FreqDist(tDWords)

## Loop through your poswords FreqDist, and calculate the
## probability of each word in the positive class, like this:
## P(word|pos) = count(word) / postok
## Store the results in poswordprobs
## USE LOGS!!!
for smileW in smileFreqDist:
    probWIsSmile = math.log(smileFreqDist[smileW] / smiletok)
    smilewordprobs[smileW] = probWIsSmile
for frownW in frownFreqDist:
    probWIsFrown = math.log(frownFreqDist[frownW] / frowntok)
    frownwordprobs[frownW] = probWIsFrown
for tUW in tUFreqDist:
    probWIstU = math.log(tUFreqDist[tUW] / tUtok)
    tUwordprobs[tUW] = probWIstU
for tDW in tDFreqDist:
    probWIstD = math.log(tDFreqDist[tDW] / tDtok)
    tDwordprobs[tDW] = probWIstD

    #########################################################
    ################# YOUR CODE ENDS HERE ###################
    #########################################################



######################################
### FUNCTIONS TO PREDICT SENTIMENT ###
######################################



## FUNCTION USING NAIVE BAYES PROBS TO PREDICT SENTIMENT
def naive_bayes(reviewwords):

    defaultprob = math.log(0.0000000000001)
    
    ### SMILE SCORE
    smilescore = smilewordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        smilescore += smilewordprobs.get(reviewwords[i], defaultprob)
    ### FROWN SCORE
    frownscore = frownwordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        frownscore += frownwordprobs.get(reviewwords[i], defaultprob)
    ### tU SCORE
    tUscore = tUwordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        tUscore += tUwordprobs.get(reviewwords[i], defaultprob)
    ### tD SCORE
    tDscore = tDwordprobs.get(reviewwords[0], defaultprob)
    for i in range(1, len(reviewwords)):
        tDscore += tDwordprobs.get(reviewwords[i], defaultprob)
        
    a = [smilescore, frownscore, tUscore, tDscore]   
    print(a)
    from operator import itemgetter
    maxPosition = min(enumerate(a), key=itemgetter(1))[0] 
    print(maxPosition)
    if maxPosition == 0:
        return 'sm'
    elif maxPosition == 1:
        return 'fr'
    elif maxPosition == 2:
        return 'tU'
    else:
        return 'tD'


#################################################
### PREDICT THE SENTIMENT OF THE TEST REVIEWS ###
#################################################

nbcorrect = 0
numberLines = 0
testdata = open("cleanTestEmojiCategory.txt", "r", encoding="utf8")
for line in testdata:

    numberLines += 1
    pol = line[0:2]
    tweet = line[4:]
    
    if pol == naive_bayes(tweet):
        nbcorrect += 1

testdata.close()

print("Naive Bayes accuracy: ", (nbcorrect/numberLines))
