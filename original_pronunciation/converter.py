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
          #print("hello")
          #print(word)
          #print("hello")
          pronounce = line[1]
          word = list(word.split("/"))# some words have a slash in them e.g. (a/an) and then some have variations denoted with a tilde ~
          pronounce = list(pronounce.split("/")) # so word splits along slashses for pronunciations
          for i in range(len(word)):
              variation = word[0]
              if pronounce[0] == '=':
                  #some words don't have pronunciations they just have equals signs
                  pronunciation = variation
              else:
                  pronunciation = pronounce[0]
              if i != 0:
                  variation = (variation + word[i][1:])
                  if len(pronounce) > i:
                      pronunciation = (pronunciation + pronounce[i][1:])
                  elif pronounce[0] == '=':
                      pronunciation = variation
                  else:
                      pronunciation = pronounce[0]
              # variation = map(lambda x : unicodedata.decimal(x), variation)
                  pronuncation = map(lambda x : unicodedata.decimal(x), pronunciation)
                  pronounce_dict[variation] = pronunciation
       #for item in pronounce_dict:
       #    print(item," ::: " ,pronounce_dict[item])


#step 2: create mapping from IPA to CMU
IPA_dict = {593:'AA', 230:'AE', 652:'AH', 596:'AO', 97:'AW', 618:'AY', 98:'B',679:'CH', 100:'D',240:'DH',603:'EH',605:'ER',0:'EY',
102:'F',103:'G',104:'HH',618:'IH',105:'IY',676:'JH',107	:'K',108:'L',109:'M',110:'N',331:'NG', 111:'OW',0:'OY',112:'P', 633:'R', 115:'S',
643	:'SH',116: 'T',952:'TH', 650:'UH',117:'UW',118:'V',119:'W',106:'Y',122:'Z', 658:'ZH'}
#step 3: convert all pronunciations in dict to CMU
word_list = list(pronounce_dict.keys())

def ipaMap(c):
    try:
        return IPA_dict[ord(c)]
    except KeyError:
        return c

for word in word_list:
    x=list(map(ipaMap, pronounce_dict[word]))
#step 4: return resulting dict to use in initial processing for all files
    print(x)
