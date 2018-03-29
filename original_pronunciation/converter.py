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

tagdict = {' abbr ':0,' adj ':0,' adv ':0,' aux ':0,' det ':0,' emend ':0,' Eng ':0,' Epil ':0,' f(f) ':0,' F ':0,
           ' interj ':0, ' Fr ':0, ' Ital ':0, ' Lat ':0, ' Luc ':0, ' m ':0, ' malap ':0, ' n ':0, ' prep ':0, ' pro ':0,
           ' Prol ':0, ' pron ':0, ' Q ':0, ' rh ':0,' s.d. ':0, ' sp ':0, ' Sp ':0, ' str ':0, ' unstr ':0, ' usu ':0,
           ' v ':0 }

taglist = [' abbr ', ' adj ', ' adv ', ' aux ', ' det ', ' emend ', ' Eng ', ' Epil ', ' f(f) ', ' F ', ' interj ',
           ' Fr ', ' Ital ', ' Lat ', ' Luc ', ' m ', ' malap ', ' n ', ' prep ', ' pro ', ' Prol ', ' pron ', ' Q ',
           ' rh ', ' s.d. ', ' sp ', ' Sp ', ' str ', ' unstr ',
           ' usu ', ' v ']

bracketTags = {}

def wordPronounceMatcher(singleword,singlepronounce):
    # if "," in pronounce:
    #     singlepronounce = singlepronounce.split(',')
    #     singlepronounce = singlepronounce[0]
    #     #print(singleword, singlepronounce)
    # if "~" in word:
    #     print(singleword, singlepronounce, "UNCAUGHT LINE", theline)
        
    pronounce_dict[singleword] = singlepronounce

with open('crystal_text.txt', encoding='UTF-8') as infile:
    for line in infile:
        line = infile.readline()
        line = line.rstrip('\n')
        line = list(line.split("|"))
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

                # wordplayregex = re.compile("[\[][\s\S^[]]*.*[\d]+[.][\d]+[.][\d]+[\]]")

                # bracketregex = re.compile("[\[][\w\s]+[\]]")
                bracketregex = re.compile("[\[][^\[\]]*[\]]")

                if re.search(bracketregex,word[i]):
                    bracketpattern = re.search(bracketregex,word[i])
                    matchedpattern = bracketpattern.group(0)
                    if matchedpattern in bracketTags:
                        bracketTags[matchedpattern] +=1
                    else:
                        bracketTags[matchedpattern] = 1
                    print ("prebracketremoval",word[i])
                    word[i] = re.sub(bracketregex, '', word[i])
                    print("post", word[i])

                # if re.search(wordplayregex, word[i])
                #     word[i] = re.sub(wordplayregex, '', word[i])

                for item in taglist:
                    if item in word[i]:
                        tagdict[item] += 1
                        word[i] = word[i].strip(item)



          

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
                                print("preplayremoval",alt)
                                alt = re.sub(playCharPattern,'',alt)
                                print("postplayremoval",alt)
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
                        print("prebracketremoval", pronounce[i])
                        pronounce[i] = re.sub(bracketregex, '', pronounce[i])
                        print("post", pronounce[i])

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
            for i in range(len(pronounce)):
                if " -" in pronounce[i]:
                    hyphenfound = True
                    endingwithouthyphen = pronounce[i].strip(" ")
                    endingwithouthyphen = endingwithouthyphen.strip("-")
                    endingwithouthyphen = endingwithouthyphen.strip(" ")
                    pronounce[i] = pronounce[0]+endingwithouthyphen
                # if hyphenfound:
                    # print("hyphenfound", word, pronounce)

            hyphentildeinprev = False
            indexofmostrecentfullword = 0

            if not dotline:
                for i in range(1,len(word)):

                    if "~" in word[i]:

                        hyphentildeinprev = True
                        endingwithouttilde = word[i]
                        endingwithouttilde = endingwithouttilde.strip(" ")
                        endingwithouttilde = endingwithouttilde.strip("~")
                        endingwithouttilde = endingwithouttilde.strip(" ")
                        # print("ending without tilde should be",endingwithouttilde)
                        word[i] = word[indexofmostrecentfullword]+endingwithouttilde

                    elif " -" in word[i]:
                        hyphentildeinprev = True
                        endingwithouthyphen = word[i].strip(" ")
                        endingwithouthyphen = endingwithouthyphen.strip("-")
                        endingwithouthyphen = endingwithouthyphen.strip(" ")
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


            # #dot words
            # elif "·" in word[0]:
            #     #print("Hello ", word[0])
            #     dotwordcount = dotwordcount + 1
            #
            #     #split the word at the dot
            #     wordSplit = word[0].split("·")
            #     if "·" in pronounce[0]:
            #         pronounceSplit = pronounce[0].split("·")
            #         pronounceRoot = pronounceSplit[0]
            #         ending = pronounceSplit[1]
            #         pronounce[0] = pronounceRoot + ending
            #         if "," in pronounce[0]:
            #             pronounce[0]=pronounce[0].split(",")
            #             pronounce[0]=pronounce[0][0]
            #     else:
            #         pronounceRoot = pronounce[0]
            #
            #     root = wordSplit[0]
            #     ending = wordSplit[1]
            #
            #     word[0]= root+ending
            #     pronounce_dict[word[0]]= pronounce[0]
            #
            #
            #     if len(word) == len(pronounce) and len(word)>1:
            #         for i in range(1, len(word)):
            #             #print (root+word[i], "   ", pronounceRoot+pronounce[i])
            #             wordVariant = root+word[i]
            #             #print(pronounceRoot, pronounce[i])
            #             pronounceVariant = pronounceRoot+pronounce[i]
            #             wordPronounceMatcher(wordVariant.strip(' '),pronounceVariant.strip(' '),line)
            #             pronounce_dict[wordVariant.strip(' ')] = pronounceVariant.strip(' ')
            #     else:
            #         mismatchcount +=1
          
            # elif "-" in pronounce[0]:
            #     if not "-" in word[0]:
            #         #print(line)
            #         #print("word",len(word),"pronounce",len(pronounce))
            #
            #         pronounce[0].strip(' m ')
            #
            #     if len(word) == len(pronounce):
            #         for i in range(len(word)):
            #             pronounce[i].strip(' ')
            #             #print(word[i], pronounce[i])
            #             wordPronounceMatcher(word[i],pronounce[i],line)
            #
            #
            #
            #     if len(word) > len(pronounce):
            #         #print(line)
            #         mismatchcount +=1
            #
            #
            #
            #     if len(word) < len(pronounce):
            #         #print(line)
            #         mismatchcount+=1
            #
            #
            #
            #
            #     altpronunciationlist = pronounce[0].split(",")
            #     pronounce[0]=altpronunciationlist[0]
            #     wordPronounceMatcher(word[0],pronounce[0],line)
            #     #print (word[0],pronounce[0])
            #     altpronunciationscount +=1
                 
            for i in range(len(word)):
                if len(word) == len(pronounce):
                    wordPronounceMatcher(word[i],pronounce[i])
                else:
                    mismatchcount+=1


               
          
         
            

                     
          
#             else:
#                 #print ("no dot!")
#                 #print("word is ", word)
#                 #print("pronounce is ", pronounce)
#                 for i in range(len(word)):
#                     #print("word is ", word)
#                     rootword = word[0]
#                     #print("variation is", variation)
#                 if pronounce[0] == '=':
#                     # some words don't have pronunciations they just have equals signs
#                     pronunciation = wordPlusVariation
#                 else:
#                     pronunciation = pronounce[0]
#                 if i != 0:
#                     wordPlusVariation = (rootword + word[i][1:])
#                     # print("variation is", wordPlusVariation)
#                     if len(pronounce) > i:
#                         pronunciation = (pronunciation + pronounce[i][1:])
#                     elif pronounce[0] == '=':
#                         pronunciation = wordPlusVariation
#                     else:
#                         pronunciation = pronounce[0]
#                     # wordPlusVariation = map(lambda x : unicodedata.decimal(x), wordPlusVariation)
#                     #pronunciation = map(lambda x : unicodedata.decimal(x), pronunciation)
#                     pronounce_dict[wordPlusVariation.strip(' ')] = pronunciation.strip(' ')
#           # for item in pronounce_dict:
# #              print(item," ::: " ,pronounce_dict[item])


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
    with open('newdict8.txt','a') as outfile:
        x=list(map(ipaMap, pronounce_dict[word]))
    #step 4: return resulting dict to use in initial processing for all files
        print(word, "    ",''.join(x))
        astring = word+ "    "+''.join(x)
        outfile.write(word + "    "+''.join(x))
        outfile.write('\n')

print ("dotwordcount is",dotwordcount)
print ("mismatchcount is", mismatchcount)
print ("abbrcount is", abbrcount)
print ("altpronunciationscount is", altpronunciationscount)
print (mlines)
print (tagdict)
print (bracketTags)