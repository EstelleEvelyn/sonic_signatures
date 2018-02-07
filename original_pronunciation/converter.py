import unicodedata

#step 1: make dict of words:pronunciations (possibly tuple values if more than one possibility)
pronounce_dict = {}
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
          
          dotwordcount = 0 
          #dot words
          if "·" in word[0]:
              print("Hello")
              dotwordcount +=1
              #split the word at the dot
              wordSplit = word[0].split("·")
              if "·" in pronounce[0]:
                  pronounceSplit = pronounce[0].split("·")
                  pronounceRoot = pronounceSplit[0]
                  ending = pronounceSplit[1]
                  pronounce[0] = pronounceRoot + ending
              else:
                  pronounceRoot = pronounce[0]
              root = wordSplit[0]
              ending = wordSplit[1]
              word[0]= root+ending
              pronounce_dict[word[0]]= pronounce[0]
              mismatchcount = 0
              if len(word) == len(pronounce) & len(word)>1:
                 for i in range(1, len(word)):
                     #print (root+word[i], "   ", pronounceRoot+pronounce[i])
                     wordVariant = root+word[i]
                     pronounceVariant = pronounceRoot+pronounce[i]
                     pronounce_dict[wordVariant.strip(' ')] = pronounceVariant.strip(' ')
              else:
                 mismatchcount +=1
              
              
          
          else:
          #print("word is ", word)
          #print("pronounce is ", pronounce)
             for i in range(len(word)):
                 #print("word is ", word)
                 rootword = word[0]
                 #print("variation is", variation)
                 if pronounce[0] == '=':
                     #some words don't have pronunciations they just have equals signs
                     pronunciation = wordPlusVariation
                 else:
                     pronunciation = pronounce[0]
                 if i != 0:
                     wordPlusVariation = (rootword + word[i][1:])
                     #print("variation is", wordPlusVariation)
                     if len(pronounce) > i:
                         pronunciation = (pronunciation + pronounce[i][1:])
                     elif pronounce[0] == '=':
                         pronunciation = wordPlusVariation
                     else:
                         pronunciation = pronounce[0]
                 # wordPlusVariation = map(lambda x : unicodedata.decimal(x), wordPlusVariation)
                     #pronunciation = map(lambda x : unicodedata.decimal(x), pronunciation)
                     pronounce_dict[wordPlusVariation.strip(' ')] = pronunciation.strip(' ')
          # for item in pronounce_dict:
#              print(item," ::: " ,pronounce_dict[item])


# step 2: create mapping from IPA to CMU
# note: 0 keys are assigned to CMU symbols that are actually represented by multiple IPA symbols
# this should be resolved in a separate mappping

IPA_dict = {593:'AA', 230:'AE', 652:'AH', 596:'AO', 97:'AW', 618:'AY', 98:'B',679:'CH', 100:'D',240:'DH',603:'EH:',605:'ER',0:'EY',
102:'F',103:'G',104:'HH',618:'IH',105:'IY',676:'JH',107	:'K',108:'L',109:'M',110:'N',331:'NG', 111:'OW',0:'OY',112:'P', 633:'R', 115:'S',
643	:'SH',116: 'T',952:'TH', 650:'UH',117:'UW',118:'V',119:'W',106:'Y',122:'Z', 658:'ZH', 629:'TH'}

# #step 3: convert all pronunciations in dict to CMU

word_list = list(pronounce_dict.keys())

def ipaMap(c):
    try:
        return IPA_dict[ord(c)]
    except KeyError:
        return c

for word in word_list:
    x=list(map(ipaMap, pronounce_dict[word]))
#step 4: return resulting dict to use in initial processing for all files
    print(word, "    ",''.join(x))

print ("dotwordcount is",dotwordcount)
print ("mismatchcount is", mismatchcount)