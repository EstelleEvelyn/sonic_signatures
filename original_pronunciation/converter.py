import unicodedata
import re

#step 1: make dict of words:pronunciations (possibly tuple values if more than one possibility)




pronounce_dict = {}
dotwordcount = 0
mismatchcount = 0
abbrcount = 0
altpronunciationscount = 0
mlines=0
abbrlines = []


#dictionary of tags
tagdict = {' abbr ':0, 'abbr ':0, ' abbr':0,  'adj':0,' adv ':0,' aux ':0,' det ':0,' emend ':0,' Eng ':0,' Epil ':0,' f(f) ':0,' F ':0,
           ' interj ':0, ' Fr ':0, ' Ital ':0, ' Lat ':0, ' Luc ':0, ' m ':0, ' malap ':0, ' n ':0, ' prep ':0, ' pro ':0,
           ' Prol ':0, ' pron ':0, ' Q ':0, ' rh ':0,' s.d. ':0, ' sp ':0, ' Sp ':0, ' str ':0, ' unstr ':0, ' usu ':0,
           ' v ':0 }

#list of tags
taglist = [' abbr ', 'abbr ', ' abbr', ' adj ', ' adv ', ' aux ', ' det ', ' emend ', ' Eng ', ' Epil ', ' f(f) ', ' F ', ' interj ',
           ' Fr ', ' Ital ', ' Lat ', ' Luc ', ' m ', ' malap ', ' n ', ' prep ', ' pro ', ' Prol ', ' pron ', ' Q ',
           ' rh ', ' s.d. ', ' sp ', ' Sp ', ' str ', ' unstr ',
           ' usu ', ' v ']

#TODO what is this???
bracketTags = {}

#TODO also what is this???
converter = {}

#TODO does this get used? And for what?
def wordPronounceMatcher(singleword,singlepronounce):
    pronounce_dict[singleword] = singlepronounce


with open('crystal_text.txt', encoding='UTF-8') as infile:
    for line in infile:
        line = infile.readline()
        line = line.rstrip('\n')
        line = list(line.split("|")) # split the word on the bar

        if len(line) > 1:

            word = line[0]
            pronounce = line[1]
            word = list(word.split("/"))# some words have a slash in them e.g. (a/an) and then some have variations denoted with a tilde ~
            pronounce = list(pronounce.split("/")) # so word splits along slashses for pronunciations

            wordlength = len(word)
            pronouncelength = len(pronounce)
            dotline = False

            for i in range(len(word)):
                word[i] = word[i].strip(" ")

                bracketregex = re.compile("[\[][^\[\]]*[\]]")

                if re.search(bracketregex, word[i]):
                    bracketpattern = re.search(bracketregex, word[i])
                    matchedpattern = bracketpattern.group(0)
                    if matchedpattern in bracketTags:
                        bracketTags[matchedpattern] +=1
                    else:
                        bracketTags[matchedpattern] = 1

                    word[i] = re.sub(bracketregex, '', word[i])

                # if re.search(wordplayregex, word[i])
                #     word[i] = re.sub(wordplayregex, '', word[i])

                if "," in word[i]:
                    altwordssplit = word[i].split(",")
                    word[i] = altwordssplit[0]

                for item in taglist:
                    if item in word[i]:
                        print("prestrip",word[i])
                        tagdict[item] += 1
                        word[i] = word[i].strip(item)
                        print("poststrip", word[i])





            altpronunciationsfound = False
            for i in range(len(pronounce)):
                playCharPattern = re.compile("^[^_]*[\d]+[.][\d]+[.][\d]+")
                bracketregex = re.compile("[\[][\w\s]+[\]]")

                if len(pronounce) >= 1:

                    # eliminate alternate pronunciations from everything
                    if "," in pronounce[i]:
                        altpronunciationsfound = True
                        # print(line)
                        # print("preprocessing", pronounce[i])
                        altpronunciationssplit = pronounce[i].split(',')


                        for alt in altpronunciationssplit:
                            if re.search(playCharPattern,alt):
                                # print("preplayremoval",alt)
                                alt = re.sub(playCharPattern,'',alt)
                                # print("postplayremoval",alt)
                                alt = alt.strip(' ')

                        if not(len(altpronunciationssplit[0]) == 0):
                            pronounce[i] = altpronunciationssplit[0]
                        else:
                            print("NOTHING IN THE ALTERNATE PRONUNCIATION")
                            pronounce[i]= altpronunciationssplit[1]
                        # print("postprocessing", pronounce[i])

                    for item in taglist:
                        if item in pronounce[i]:
                            tagdict[item] += 1
                            pronounce[i] = pronounce[i].strip(item)

                    if re.search(playCharPattern, pronounce[i]):
                        pronounce[i]= re.sub(playCharPattern, '', pronounce[i])

                    if re.search(bracketregex, pronounce[i]):
                        bracketpattern = re.search(bracketregex, pronounce[i])
                        matchedpattern = bracketpattern.group(0)
                        if matchedpattern in bracketTags:
                            bracketTags[matchedpattern] += 1
                        else:
                            bracketTags[matchedpattern] = 1
                        # print("prebracketremoval", pronounce[i])
                        pronounce[i] = re.sub(bracketregex, '', pronounce[i])
                        # print("post", pronounce[i])

                    # eliminate stress tags from everything
                    if "str" in pronounce[i]:
                        pronounce[i] = pronounce[i].strip(" str ")

                        # print("postSTRprocessing", pronounce[i])

                    # eliminate meter tags from everything
                    if " m " in pronounce[i]:
                        pronounce[i] = pronounce[i].strip(" m ")
                        # print("postMprocessing", pronounce[i])


            # deal with all dot words
            numdots = 0
            for i in range(len(word)):
                if "·" in word[i]:
                    dotline = True
                    numdots +=1
                    #print(word[i])
                    # if numdots > 1:
                    #     # print("numdots exception", word, pronounce)

            if "·" in word[0]:
                dotwordcount = dotwordcount + 1
                # print("predotprocessing", word, pronounce)


                # split the word at the dot
                wordSplit = word[0].split("·")

                root = wordSplit[0]
                ending = wordSplit[1]
                ending = ending.strip(" ")
                ending = ending.strip("~")
                ending = ending.strip("-")
                ending = ending.strip(" ")

                word[0] = root + ending

                for i in range(1,len(word)):
                    word[i] = word[i].strip(" ")
                    word[i] = word[i].strip("~")
                    word[i] = word[i].strip("-")
                    word[i] = word[i].strip(" ")
                    word[i] = root+word[i]

                # print("postdotprocessing", word, pronounce)

            if "·" in pronounce[0]:
                pronounceSplit = pronounce[0].split("·")

                pronounceRoot = pronounceSplit[0].strip(" ")
                pronounceEnding = pronounceSplit[1]
                pronounceEnding = pronounceEnding.strip(" ")
                pronounceEnding = pronounceEnding.strip("-")
                pronounceEnding = pronounceEnding.strip("~")
                pronounceEnding = pronounceEnding.strip(" ")

                pronounce[0] = pronounceRoot + pronounceEnding

                for i in range(1,len(pronounce)):
                    pronounce[i] = pronounceRoot + pronounce[i]

                # print("postdotprocessing", word, pronounce)


            # deal with all tilde words
            hyphenfound = False
            hyphenending = re.compile("\A[^\w]*[-][\w]+")
            for i in range(len(pronounce)):
                # if "-" in pronounce[i]:
                #     print(pronounce[i])
                if re.search(hyphenending,pronounce[i]):
                    hyphenfound = True
                    # print(pronounce[i])
                    endingwithouthyphen = re.sub("[-]",'',pronounce[i])
                    endingwithouthyphen = endingwithouthyphen.strip(" ")
                    pronounce[0] = pronounce[0].strip(" ")
                    pronounce[i] = pronounce[0]+endingwithouthyphen
                # if hyphenfound:
                #     print("hyphenfound", word, pronounce[i])

            hyphentildeinprev = False
            indexofmostrecentfullword = 0

            if not dotline:
                for i in range(1,len(word)):

                    tildeending = re.compile("\A[^\w]*[~][\w]+")
                    if re.search(tildeending, word[i]):

                        hyphentildeinprev = True
                        endingwithouttilde = word[i]
                        endingwithouttilde = endingwithouttilde.strip(" ")
                        endingwithouttilde = endingwithouttilde.strip("~")
                        endingwithouttilde = endingwithouttilde.strip(" ")
                        endingwithouttilde = re.sub("[~]",'',endingwithouttilde)
                        # print("ending without tilde should be",endingwithouttilde)
                        word[i] = word[indexofmostrecentfullword]+endingwithouttilde

                    elif re.search(hyphenending,word[i]):
                        hyphentildeinprev = True
                        endingwithouthyphen = word[i].strip(" ")
                        endingwithouthyphen = endingwithouthyphen.strip("-")
                        endingwithouthyphen = endingwithouthyphen.strip(" ")
                        endingwithouthyphen = re.sub("[-]",'',endingwithouthyphen)
                        word[i] = word[indexofmostrecentfullword]+endingwithouthyphen

                    elif re.match("\s[\w]\s", word[i]):
                        hyphentildeinprev = True
                        # print("Myregexmatched",word[i])
                        word[i] = word[indexofmostrecentfullword]+word[i]

                    elif hyphentildeinprev:
                        # print("NEW MOST RECENT FULL WORD", word[i])
                        # print(word,pronounce)
                        hyphentildeinprev = False
                        indexofmostrecentfullword = i

                # if hyphentildeinprev:
                #     print(word, pronounce)

            if len(word) > 1 and len(pronounce) == 1:
                if pronounce[0] == " =":
                    for i in range(1, len(word)):
                        pronounce.append(" = ")
                    # print(word, pronounce)

            if len(word) > 1 and "~s" in word[1]:
                # if "~s" in word[1]:
                if len(pronounce) < len(word):
                    # print("pluralcase", word, pronounce)
                    root = word[0]
                    s = word[1].strip(" ")
                    s = s.strip("~")
                    s = s.strip(" ")

                    # pluralword = root.strip(' ') + s
                    # word[1] = pluralword
                    singularpronounce = pronounce[0].strip(" ' ")
                    singularpronounce = singularpronounce.strip('z')
                    pluralpronounce = pronounce[0]
                    pronounce[0] = singularpronounce
                    pronounce.append(pluralpronounce)
                    # print("pluralcase", word, pronounce)
                # if "=" in pronounce[0]:
                #     pronounce_dict[root.strip(' ')] = pronounce[0]
                #     pronounce_dict[pluralword] = pronounce[0]

            for item in word:
                if " ~" in item:
                    # print(word)
                    item = item.strip(" ")
                    item = item.strip("~")
                    item = item.strip(" ")
                    # print("tilde should have been removed", item)

                if " -" in item:
                    item = item.strip(" ")
                    item = item.strip("-")
                    item = item.strip(" ")

            for i in range(len(word)):
                if len(word) == len(pronounce):
                    wordPronounceMatcher(word[i],pronounce[i])
                else:
                    mismatchcount+=1


# step 2: create mapping from IPA to CMU
# note: 0 keys are assigned to CMU symbols that are actually represented by multiple IPA symbols
# this should be resolved in a separate mappping

IPA_dict = {593:'AA', 230:'AE', 652:'AH', 596:'AO', 97:'AW', 618:'AY', 98:'B',679:'CH', 100:'D',240:'DH',603:'EH:',605:'ER',0:'EY',
102:'F',103:'G',104:'HH',618:'IH',105:'IY',676:'JH',107	:'K',108:'L',109:'M',110:'N',331:'NG', 111:'OW',0:'OY',112:'P', 633:'R', 115:'S',
643	:'SH',116: 'T',952:'TH', 650:'UH',117:'UW',118:'V',119:'W',106:'Y',122:'Z', 658:'ZH', 629:'TH'}

# #step 3: convert all pronunciations in dict to CMU

word_list = list(pronounce_dict.keys())
word_list.sort()

def ipaMap(c):
    try:
        return IPA_dict[ord(c)]
    except KeyError:
        return c

for word in word_list:
    with open('newdict17.txt','a') as outfile:
        x=list(map(ipaMap, pronounce_dict[word]))
    #step 4: return resulting dict to use in initial processing for all files
        # print(word, "    ",''.join(x))
        astring = word+ "    "+' '.join(x)
        capsword = word.upper()
        outfile.write(capsword + " ; "+' '.join(x))
        outfile.write('\n')
        converter[capsword] = ' '.join(x)
    # with open('wordlist.txt', 'a') as wordlistfile:
    #     wordlistfile.write(word)
    #     wordlistfile.write('\n')

# print ("dotwordcount is",dotwordcount)
# print ("mismatchcount is", mismatchcount)
# print ("abbrcount is", abbrcount)
# print ("altpronunciationscount is", altpronunciationscount)
# print (mlines)
# print (tagdict)
# print (bracketTags)