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
        self.omission_dict = {}
        self.word_count = 0

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
        for i in range(len(word)):
            # print(word[i])
            if word[i] in vowel_letters:
                # print("is in vowel letters")
                if not prevWasVowel and tba != '':
                    word_split_on_vowels.append(tba)
                    # print("added ", tba)
                    tba = ''
                tba += word[i]
                # print("tba now equals",tba)
                prevWasVowel = True
            else:
                if prevWasVowel:
                    word_split_on_vowels.append(tba)
                    # print("added ", tba)
                    tba = ''
                tba += word[i]
                # print("tba is now", tba)
                prevWasVowel = False
            # print(i, len(word)-1)
            if i == len(word)-1:
                word_split_on_vowels.append(tba)
                # print("added", tba)

        # print(word, word_split_on_vowels)

        return word_split_on_vowels

    def matchVowelsWithTokens(self, word, tokenizedWord):
        split_pronunciation = tokenizedWord.split(' ')
        if len(word) == len(split_pronunciation):
            for i in range(len(word)):
                print(word[i], split_pronunciation[i])

        elif len(word) < len(split_pronunciation):
            print("MORE TOKENS IN PRONUNCIATION", word, split_pronunciation)

        else:
            print("FEWER TOKENS IN PRONUNCIATION", word, split_pronunciation)




    def phonetic_transcript(self, file_name):
        '''
        Takes the name of a text file in the res file and writes a phonetic transcription
        of that file to the destination folder
        '''
        root = nltk.data.find('/')
        with open('res/{}.txt'.format(file_name), 'r') as corpus:  # source file
            with open('tagtext/{}_orig.csv'.format(file_name), 'a') as dest_file:  # destination
                corpus_text = corpus.read().lower().split()  # normalize
                for word in corpus_text:
                    self.word_count += 1
                    # for char in string.punctuation:
                    #                         word = word.replace(char,"")
                    #                     print(self.OP)
                    #                     print(self.OP[word])
                    if word in self.OP:  # TODO find a better way to resolve non-standard words
                        print("word in self.OP: ", word)
                        if '=' in self.OP[word]:
                            if word in self.transcr:  # TODO find a better way to resolve non-standard words
                                phonetic_list = self.transcr[word][0]
                                phonetic_string = ""
                                for sound in phonetic_list:  # this is inefficient
                                    sound = sound.strip(":")
                                    sound = sound.strip("'")
                                    if ":" not in sound and "'" not in sound:
                                        phonetic_string = phonetic_string + sound + " "
                                phonetic_string = phonetic_string.strip()
                                split_word = self.split_along_consonants_and_vowels(word)
                                self.matchVowelsWithTokens(split_word, phonetic_string)
                                # dest_file.write(word + ", " + phonetic_string + ", " + "s"+", " + "\n")
                        else:
                            phonetic_list = self.OP[word].split(" ")
                            # print(phonetic_list)
                            # phonetic_string=""
                            # for sound in phonetic_list: #this is inefficient
                            #     phonetic_string = phonetic_string+sound+" "
                            phonetic_string = ""
                            for sound in phonetic_list:  # this is inefficient
                                sound = sound.strip(":")
                                sound = sound.strip("'")
                                if ":" not in sound and "'" not in sound:
                                    phonetic_string = phonetic_string + sound + " "
                            phonetic_string = phonetic_string.join("").strip()
                            split_word = self.split_along_consonants_and_vowels(word)
                            self.matchVowelsWithTokens(split_word,phonetic_string)
                            # dest_file.write(word + ", " + phonetic_list + ", " + "s"+", " + "\n")
                    elif word in self.transcr:  # TODO find a better way to resolve non-standard words
                        phonetic_list = self.transcr[word][0]
                        phonetic_string = ""
                        for sound in phonetic_list:  # this is inefficient
                            phonetic_string = phonetic_string + sound + " "
                        split_word = self.split_along_consonants_and_vowels(word)
                        phonetic_string = phonetic_string.strip()
                        self.matchVowelsWithTokens(split_word, phonetic_string)
                        # dest_file.write(word+", "+ phonetic_string + ", " + "s" + ", " + "\n")
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
    # tagtext.split_along_consonants_and_vowels("corbo")
    tagtext.get_OP()
    tagtext.get_all_character_texts()
    #transcriber.omission_printer()

if __name__ == "__main__":
    main()