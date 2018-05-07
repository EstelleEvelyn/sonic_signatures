"""
create tagtext format for serendip text visualization

format token, tokenToMatch, endreason, topic_X

token is simply the unchanged token from the document.

tokenToMatch is the simplified token used to match it to corresponding
tokens during modeling. Generally, this is done through lowercasing,
but can include more complex things like lemmatizing.

endReason is the event that cut off the token,
and can have values of s for a space, c for a character like punctuation, and n for a newline.

topic_X (replacing x for the number of the topic) indicates the topic that this word is tagged with. This value is optional, as not every word will necessarily get tagged (e.g., stopwords will not).
"""

import nltk
from nltk.corpus import cmudict
import urllib
from bs4 import BeautifulSoup
import unicodedata

class Tagtext:

    def __init__(self):
        self.transcr = cmudict.dict()  # import cmudict

        self.OP = {}

        # conv = converter.Converter()
        # self.or_transcr = conv.getDict()

        self.play_code_list = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4',
                               'H5', '1H6', '2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac',
                               'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
                               'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']
        self.vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
        self.OpheliaVowels = ['IH', 'IY', 'EY', 'AY','AE','UW','UH','AA','AO']
        self.omission_dict = {}
        self.word_count = 0
        self.misses = 0
        self.correct = 0

    def get_character_list(self, play):
        '''
        Takes a play key for a Shakespeare play and returns a list containing the
        characters in that play
        '''

        base_url = 'http://www.folgerdigitaltexts.org/{}/charText/'
        url = base_url.format(play)

        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        html_data = BeautifulSoup(string_from_server, "html.parser")
        character_list = []
        words_and_chars = html_data.find_all('div')
        for i in range(3, len(words_and_chars)):
            if i % 2 == 1:
                character_list.append(words_and_chars[i].text)
        return character_list

    def get_OP(self):
        with open('../original_pronunciation/newdict17.txt', 'r') as opfile:
            for line in opfile:
                worddef = line.split(';', 1)
                # print(worddef[0].lower())
                if len(worddef) > 1:
                    self.OP[worddef[0].lower().strip()] = worddef[1].strip().strip('\n')
                else:
                    print("length was too long" + ''.join(worddef))
        # print(self.OP)

    def normalize_caseless(self,text):
       return unicodedata.normalize("NFKD", text.casefold())

    def caseless_equal(left, right):
       return normalize_caseless(left) == normalize_caseless(right)

    def split_along_consonants_and_vowels(self, word):
        vowel_letters = ['a', 'e', 'i', 'o', 'u']

        word_split_on_vowels =[]
        tba = ''
        prevWasVowel = False
        prevWasT = False
        prevWasS = False
        prev = None
        for i in range(len(word)):
            # print(word[i])
            if word[i] in vowel_letters:
                # print("is in vowel letters")

                if not prevWasVowel and tba != '':
                    if (i == len(word) - 1) and word[i] == 'e':
                        if len(word_split_on_vowels) < 1:
                            word_split_on_vowels.append(tba)
                            tba = ''
                        else:
                            # print(word_split_on_vowels)
                            word_split_on_vowels[-1] = prev+'e'
                            continue
                    else:
                        word_split_on_vowels.append(tba)
                        # print("didn't add in the vowel loop", tba)
                        tba = ''
                tba += word[i]
                # print("tba now equals",tba)

                prevWasVowel = True
                prev = word[i]
            else:
                if prevWasVowel:
                    word_split_on_vowels.append(tba)
                    tba = ''
                    prev = None

                # if (i != len(word)-1) and word[i] == 't':
                #     tba += word[i]
                #     continue
                #
                # if (i != len(word)-1) and word[i] == 's':
                #     tba += word[i]
                #     continue



                if prev == 'c' and word[i] == 'k':
                    # print("appending ck")
                    word_split_on_vowels.append('ck')
                    tba = ''

                elif prev == 's' and word[i] == 'h':
                    # print("appending sh")
                    word_split_on_vowels.append('sh')
                    tba = ''

                elif prev == 'c' and word[i] == 'h':
                    # print("appending ch")
                    word_split_on_vowels.append('ch')
                    tba = ''

                elif prev == 't' and word[i] == 'h':
                    # print("appending th")
                    word_split_on_vowels.append('th')
                    tba = ''

                elif prev == 's' and word[i] == 'c':
                    # print("appending sc")
                    word_split_on_vowels.append('sc')
                    tba = ''

                elif prev == 'q' and word[i] == 'u':
                    # print("appending qu")
                    word_split_on_vowels.append('qu')
                    tba = ''

                elif prev == 'w' and word[i] == 'h':
                    # print("appending wh")
                    word_split_on_vowels.append('wh')
                    tba = ''

                elif prev == 'w' and word[i] == 'r':
                    # print("appending wh")
                    word_split_on_vowels.append('wr')
                    tba = ''

                elif prev == word[i]:
                    # print("appending prev plus word[i]")
                    word_split_on_vowels.append(prev+word[i])
                    tba = ''

                elif prev is None:
                   tba+= word[i]
                   pass

                else:
                    word_split_on_vowels.append(prev)
                    tba = ''
                    tba += word[i]

                prevWasVowel = False

                if word[i] == 't':
                    prevWasT = True
                elif word[i] == 's':
                    prevWasS = True
                prev = word[i]

            # print(i, len(word)-1)
            if (i == len(word)-1) and (tba != ''):
                word_split_on_vowels.append(tba)
                # print("added at the end", tba)

        # print(word, word_split_on_vowels)

        return word_split_on_vowels

    def matchVowelsWithTokens(self, word, tokenizedWord):
        split_pronunciation = tokenizedWord.strip().split(' ')
        if len(word) == len(split_pronunciation):
            # print("SAME", word, split_pronunciation, word.append(split_pronunciation))
            topics = []
            for phoneme in split_pronunciation:
                if phoneme in self.OpheliaVowels:
                    topics.append(phoneme)
            returnobject = [word,split_pronunciation,topics]
            print(returnobject)
            self.correct +=1
            # print([word.append(split_pronunciation)])
            return returnobject

        elif len(word) < len(split_pronunciation):
            # print("MORE TOKENS IN PRONUNCIATION", word, split_pronunciation)
            self.misses += 1

        else:
            # print("FEWER TOKENS IN PRONUNCIATION", word, split_pronunciation)
            self.misses += 1


    def phonetic_transcript(self, file_name):
        '''
        Takes the name of a text file in the res file and writes a phonetic transcription
        of that file to the destination folder
        '''
        root = nltk.data.find('/')
        with open('res/{}.txt'.format(file_name), 'r') as corpus:  # source file
            with open('tagtext/{}_orig1.csv'.format(file_name), 'a') as dest_file:  # destination
                corpus_text = corpus.read().lower().split()  # normalize
                for word in corpus_text:
                    self.word_count += 1
                    # for char in string.punctuation:
                    #                         word = word.replace(char,"")
                    #                     print(self.OP)
                    #                     print(self.OP[word])
                    if word in self.OP:  # TODO find a better way to resolve non-standard words
                        # print("word in self.OP: ", word)
                        if '=' in self.OP[word]:
                            if word in self.transcr:  # TODO find a better way to resolve non-standard words
                                phonetic_list = self.transcr[word][0]
                                phonetic_string = ""
                                for sound in phonetic_list:  # this is inefficient
                                    if (not sound == ":") and (not sound == ":") and (not sound == "ˈ") and (not sound == "ˈ"):
                                        sound = sound.strip(":")
                                        sound = sound.strip("'")
                                        sound = sound.strip("0123456789")
                                        phonetic_string = phonetic_string + sound + " "
                                phonetic_string = phonetic_string.strip()
                                # print("phonetic string:", phonetic_string, "phonetic list:", phonetic_list)
                                split_word = self.split_along_consonants_and_vowels(word)
                                taco = (self.matchVowelsWithTokens(split_word, phonetic_string))
                                if taco is not None and taco[0] is not None:
                                    dest_file.write(
                                        "".join(taco[0]) + "," + "'" + ",".join(taco[1]) + "'" + ", " + "s" + ", " +",".join(taco[2])+ "\n")
                        else:
                            phonetic_list = self.OP[word].split(" ")
                            # print(phonetic_list)
                            # print(phonetic_list)
                            # phonetic_string=""
                            # for sound in phonetic_list: #this is inefficient
                            #     phonetic_string = phonetic_string+sound+" "
                            phonetic_string = ""
                            for sound in phonetic_list:  # this is inefficient
                                if (not sound == ":") and (not sound == ":") and (not sound == "ˈ") and (not sound == "ˈ"):
                                    sound = sound.strip(":")
                                    sound = sound.strip("'")
                                    sound = sound.strip("1234567890")
                                    phonetic_string = phonetic_string + sound + " "
                                # else:
                                #     print(sound)
                            # phonetic_string = (" ").join(phonetic_list).strip()
                            # print(phonetic_string)
                            split_word = self.split_along_consonants_and_vowels(word)

                            taco = (self.matchVowelsWithTokens(split_word, phonetic_string))
                            if taco is not None and taco[0] is not None:
                                dest_file.write(
                                    "".join(taco[0]) + "," + "'" + ",".join(taco[1]) + "'" + ", " + "s" + ", " +",".join(taco[2])+ "\n")
                    elif word in self.transcr:  # TODO find a better way to resolve non-standard words
                        phonetic_list = self.transcr[word][0]
                        phonetic_string = ""
                        for sound in phonetic_list:  # this is inefficient
                            sound = sound.strip("1234567890")
                            phonetic_string = phonetic_string + sound + " "
                        split_word = self.split_along_consonants_and_vowels(word)
                        phonetic_string = phonetic_string.strip()
                        taco = (self.matchVowelsWithTokens(split_word, phonetic_string))
                        print(taco, type(taco))
                        if taco is not None and taco[0] is not None:
                            dest_file.write(
                                "".join(taco[0]) + "," + "'" + ",".join(taco[1]) + "'" + ", " + "s" + ", " +",".join(taco[2])+ "\n")
                    # this was for omission finder testing
                    else:
                        word = self.normalize_caseless(word)

                        if word in self.omission_dict:
                            self.omission_dict[word] += 1
                        else:
                            self.omission_dict[word] = 1

    def get_all_character_texts(self):
        '''
        Gets every text for every character in every Shakespeare play and writes it to
        a file in the res folder, then writes the phonetic transcription to the dest
        folder
        '''

        for play in self.play_code_list:
            character_list = self.get_character_list(play)
            for character in character_list:
                # self.get_character_text(play, character)
                self.phonetic_transcript(play + "_" + character)
def main():

    tagtext = Tagtext()
    # tagtext.split_along_consonants_and_vowels("access")

    tagtext.get_OP()
    tagtext.get_all_character_texts()
    print("misses: ", tagtext.misses, "correct: ", tagtext.correct)

    #transcriber.omission_printer()

if __name__ == "__main__":
    main()