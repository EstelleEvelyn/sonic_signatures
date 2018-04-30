import os
worddict = {}
wordlist = []

with open('wordlist.txt', 'r') as wordlistfile:
    for line in wordlistfile:
        word = line.strip().lower()
        worddict[word] = 0
        wordlist.append(word)

for filename in os.listdir("../tagging/res"):
    with open("../tagging/res/{}".format(filename),'r') as foliotext:
        foliocontents = foliotext.readlines()
        for line in foliocontents:
            line = line.split(' ')
            for word in line:
                if word.strip().lower() in worddict:
                    worddict[word.strip().lower()] +=1

d_view = [ (v,k) for k,v in worddict.items() ]
d_view.sort(reverse=True) # natively sort tuples by first element
with open('plausibility2.txt','a') as outfile:
    for v,k in d_view:
        print("%s: %d" % (k,v))
        outfile.write("%s: %d" % (k,v))
        outfile.write("\n")
