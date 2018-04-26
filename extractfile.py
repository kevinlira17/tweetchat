import sys
import os

def extractData(tweetdata):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    with open(tweetdata, 'r', encoding="utf-8") as readfile:
        count = 1
        for line in readfile:
            with open(os.path.join('/Users/kevinlira/NLP/Testdata',"test" + str(count) + ".txt"), 'w', encoding="utf-8") as f:
                f.write(line)
                print(line.translate(non_bmp_map))
            count += 1

def formatResult(tweetdata, resdata):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    tweetlist = []
    reslist = []
    with open(tweetdata, 'r', encoding="utf-8") as readfile:
        for line in readfile:
            tweetlist.append(line)
    with open(resdata, 'r', encoding="utf-8") as readfile:
        for line in readfile:
            words = line.split()
            if (words[2] != "posemo"):
                if (float(words[2]) > float(words[3])):
                    reslist.append("pos")
                elif(float(words[2]) < float(words[3])):
                    reslist.append("neg")
                else:
                    reslist.append("neu")
    with open("resdata.txt", 'w', encoding="utf-8") as save:
        for i in range(len(tweetlist)):
            save.write(reslist[i] + " " + tweetlist[i] + "\n")

#extractData("cleanTestData.txt")
#formatResult("cleanTestData.txt", "LIWC2015res.txt")
