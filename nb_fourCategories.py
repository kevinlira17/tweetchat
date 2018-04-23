
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
