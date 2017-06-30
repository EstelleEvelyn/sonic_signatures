import nltk
from nltk.corpus import cmudict
import sys
import argparse
import urllib.request
import json
from bs4 import BeautifulSoup #toggle comment for this line if bs4 not installed
import string
import unicodedata



'''
phonetic_transcriber.py
@author Estelle Bayer, Summer 2017
A program which uses the Folger Shakespeare API and the nltk pronuncation dictionary
to produce resource files containing text for every speaking character in every play
and destination files of the phonetic transcriptions of those same files
'''

#TODO efficiency optimization
class Transcriber:

    def __init__(self):
        self.transcr = cmudict.dict() #import cmudict

        self.play_code_list = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4',
                                'H5', '1H6', '2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac',
                                'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
                                'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']
        self.omission_dict = {}
        self.word_count = 0

    def get_play_code_list(self):
        return self.play_code_list

    def get_character_text(self, play, character):
        '''
        Takes the name of a Shakespeare play key and character in that play, and uses the
        Folger API to write that character's text to a file in the res folder
        '''

        character_tag = play+"_"+character

        base_url = 'http://www.folgerdigitaltexts.org/{0}/charText/{1}.html'
        url = base_url.format(play, character_tag)

        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        string_from_server.encode('ascii', 'replace')
        initial_text = BeautifulSoup(string_from_server, 'html.parser')
        for tag in initial_text.findAll('br'):
            tag.replace_with('\n')

        with open ('C:/Accounts/bayere/Desktop/sonic_signatures/res/{}.txt'.format(character_tag), 'w') as res_file:
            for line in initial_text.find_all('body'):
                write_string = line.text
                #TODO try to fix this mapping
                # punctuation_string = string.punctuation.replace("'", "")
                # punctuation_string = string.punctuation.replace("-", "")
                # write_string.translate(str.maketrans("\u2019", "'", punctuation_string))
                new_string = ""
                for character in write_string: #a pretty inefficient loop that only preserves readable text
                    if character.lower() in "abcdefghijklmnopqrstuvwxyz \n-":
                        new_string += character
                    if character == "\u2019":
                        new_string += "'"
                res_file.write(new_string)



    def get_character_list(self, play):
        '''
        Takes a play key for a Shakespeare play and returns a list containing the
        characters in that play
        '''

        base_url = 'http://www.folgerdigitaltexts.org/{}/charText/'
        url  = base_url.format(play)

        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        html_data = BeautifulSoup(string_from_server, "html.parser")
        character_list = []
        words_and_chars = html_data.find_all('div')
        for i in range(3, len(words_and_chars)):
            if i % 2 == 1:
                character_list.append(words_and_chars[i].text)
        return character_list

    def normalize_caseless(self,text):
       return unicodedata.normalize("NFKD", text.casefold())

    def caseless_equal(left, right):
       return normalize_caseless(left) == normalize_caseless(right)


    def phonetic_transcript(self, file_name):
        '''
        Takes the name of a text file in the res file and writes a phonetic transcription
        of that file to the destination folder
        '''
        root = nltk.data.find('/')
        with open('res/{}.txt'.format(file_name), 'r') as corpus: #source file
            with open('dest/{}.txt'.format(file_name), 'w') as dest_file: #destination
                corpus_text = corpus.read().lower().split() #normalize
                for word in corpus_text:
                    self.word_count +=1
                    # for char in string.punctuation:
#                         word = word.replace(char,"")
                    if word in self.transcr: #TODO find a better way to resolve non-standard words
                        phonetic_list = self.transcr[word][0]
                        phonetic_string=""
                        for sound in phonetic_list: #this is inefficient
                            phonetic_string = phonetic_string+sound+" "
                        dest_file.write(phonetic_string+", ")
                    # this was for omiission finder testing
                    else:
                         word = self.normalize_caseless(word)

                         if word in self.omission_dict:
                            self.omission_dict[word]+=1
                         else:
                            self.omission_dict[word] = 1



    def omission_printer(self):
       '''
       Prints the omissions into a file
       '''
       tacofile = open('keys.txt','a')
       keydict = {}
       with open('omissionsWITHPUNCTUATION.txt','a') as dest:
           for key in self.omission_dict.keys():
               if not key in keydict:
                  keydict[key] = 1
               else:
                  keydict[key] +=1

               #tacofile.write(key + ",")
               #for char in key:
                  #tacofile.write(unicodedata.name(char)+",")
               #tacofile.write("\n")
               dest.write(str(key) + "," + str(self.omission_dict[key]) + "\n")



    def get_all_character_texts(self):
        '''
        Gets every text for every character in every Shakespeare play and writes it to
        a file in the res folder, then writes the phonetic transcription to the dest
        folder
        '''

        for play in self.play_code_list:
            character_list = self.get_character_list(play)
            for character in character_list:
                #self.get_character_text(play, character)
                self.phonetic_transcript(play+"_"+character)




def main():
    transcriber = Transcriber()
    transcriber.get_all_character_texts()
    print(transcriber.word_count)
    #transcriber.omission_printer()

if __name__ == "__main__":
    main()
