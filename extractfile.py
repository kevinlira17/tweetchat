import sys
import os

def checkTweetSize(tweetdata):
    with open(tweetdata, 'r', encoding="utf-8") as f:
        for i, l in enumerate(f):
            pass
    print(i + 1)

def extractData(tweetdata):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    with open(tweetdata, 'r', encoding="utf-8") as readfile:
        count = 1
        for line in readfile:
            with open(os.path.join('/Users/kevinlira/NLP/Testdata', str(count) + ".txt"), 'w', encoding="utf-8") as f:
                f.write(line)
                print(line.translate(non_bmp_map))
            count += 1

def formatResult(tweetdata, resdata):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    tweetlist = []
    resmap = {}
    with open(tweetdata, 'r', encoding="utf-8") as readfile:
        for line in readfile:
            tweetlist.append(line)
    with open(resdata, 'r', encoding="utf-8") as readfile:
        for line in readfile:
            words = line.split()
            fileval = words[0].strip(".txt")
            if (words[2] != "posemo"):
                if (float(words[2]) > float(words[3])):
                    resmap[fileval] = "1"
                elif(float(words[2]) < float(words[3])):
                    resmap[fileval] = "0"
                else:
                    resmap[fileval] = "-1"
    with open("resdata.txt", 'w', encoding="utf-8") as save:
        for i in range(len(tweetlist)):
            save.write(resmap[str(i+1)] + " " + tweetlist[i] + "\n")
    print("complete")

#checkTweetSize("cleanTestData.txt")
#extractData("cleanTestData.txt")
#formatResult("cleanTestData.txt", "LIWC2015res.txt")
