from nltk_sonic_tagging import Transcriber
import math

'''
text_classifier.py
@authors Estelle Bayer, Liz Nichols, Summer 2017
A program that, given an ARPAbet source file, returns a dictionary containing the
number of occurrences of a handful of linguistic classifications
'''

class Tagger:
    def __init__(self):
        #a dictionary with rudimentary classifications of every phoneme in our source files
        self.consonant_classifier_dictionary = {
            'B':['stop', 'bilabial', 'voiced', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'CH':['affricate', 'linguaalveolar', 'voiceless', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'D':['stop', 'linguaalveolar', 'voiced', 'nonsibilant', 'nonsonorant', 'coronal'],
            'DH':['fricative', 'linguadental', 'voiced', 'nonsibilant', 'nonsonorant', 'coronal'],
            'F':['fricative', 'labiodental', 'voiceless', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'G':['stop', 'linguavelar', 'voiced', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'HH':['fricative', 'glottal', 'voiceless', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'JH':['affricate', 'linguaalveolar', 'voiced', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'K':['stop', 'linguavelar', 'voiceless', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'L':['liquid', 'linguaalveolar', 'voiced', 'nonsibilant', 'sonorant', 'coronal'],
            'M':['nasal', 'bilabial', 'voiced', 'nonsibilant', 'sonorant', 'noncoronal'],
            'N':['nasal', 'linguaalveolar', 'voiced', 'nonsibilant', 'sonorant', 'noncoronal'],
            'NG':['nasal', 'linguavelar', 'voiced', 'nonsibilant', 'sonorant', 'coronal'],
            'P':['stop', 'bilabial', 'voiceless', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'R':['liquid', 'linguapalatal', 'voiced', 'nonsibilant', 'sonorant', 'coronal'],
            'S':['fricative', 'linguaalveolar', 'voiceless', 'sibilant', 'nonsonorant', 'coronal'],
            'SH':['fricative', 'linguapalatal', 'voiceless', 'sibilant', 'nonsonorant', 'coronal'],
            'T':['stop', 'linguaalveolar', 'voiceless', 'nonsibilant', 'nonsonorant', 'coronal'],
            'TH':['fricative', 'linguadental', 'voiceless', 'nonsibilant', 'nonsonorant', 'coronal'],
            'V':['fricative', 'labiodental', 'voiced', 'nonsibilant', 'nonsonorant', 'noncoronal'],
            'W':['glide', 'bilabial', 'voiced', 'nonsibilant', 'sonorant', 'noncoronal'],
            'Y':['glide', 'linguapalatal', 'voiced', 'nonsibilant', 'sonorant', 'noncoronal'],
            'Z':['fricative', 'linguaalveolar', 'voiced', 'sibilant', 'nonsonorant', 'coronal'],
            'ZH':['fricative', 'linguapalatal', 'voiced', 'sibilant', 'nonsonorant', 'coronal']
            }
        self.vowel_classifier_dictionary = {
            'AA':['monophthong', 'back', 'unrounded', 'lax'],
            'AE':['monophthong', 'front', 'unrounded', 'lax'],
            'AH':['monophthong', 'central', 'unrounded', 'lax'],
            'AO':['monophthong', 'back', 'rounded', 'lax'],
            'AW':['diphthong'],
            'AY':['diphthong'],
            'EH':['monophthong', 'front', 'unrounded', 'lax'],
            'ER':['monophthong', 'central', 'rounded','tense'],
            'EY':['diphthong'],
            'IH':['monophthong', 'front', 'unrounded', 'lax'],
            'IY':['monophthong', 'front', 'unrounded', 'tense'],
            'OW':['diphthong'],
            'OY':['diphthong'],
            'UH':['monophthong', 'back', 'rounded', 'lax'],
            'UW':['monophthong', 'back', 'rounded', 'tense']
            }

        self.global_consonants = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
            'stop':0, 'glottal':0, 'linguaalveolar':0, 'linguapalatal':0,
            'labiodental':0, 'bilabial':0, 'linguavelar':0,'linguadental':0,
            'voiced':0, 'voiceless':0, 'sibilant':0, 'nonsibilant':0,
            'sonorant':0, 'nonsonorant':0, 'coronal':0, 'noncoronal':0}
        self.global_vowels = {'monophthong':0, 'diphthong':0, 'central':0, 'front':0, 'back':0,
            'tense':0, 'lax':0, 'rounded':0,'unrounded':0}

        self.consonant_count = 0
        self.vowel_count = 0

    def phoneme_frequency(self, read_file):
       ''' most of the research on phonemes in speech comes not from the distinctive
       features of phonemes used but from the phonemes themselves - counts the number of
       each phoneme and assesses the frequencies of each'''

       countingDict = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
       'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
       'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
       'DH':0,'D':0,'CH':0}
       percentageDict = {}

       totalPhonemeCount = 0

       with open("dest/{}.txt".format(read_file), 'r') as source:
           text = source.read().split()
           for phoneme in text:
               totalPhonemeCount +=1
               if phoneme[-1] in '0123456789':
                   phoneme = phoneme[:-1]
               if phoneme in countingDict:
                   countingDict[phoneme]+=1

       for item in countingDict:
           if countingDict.get(item)!= None:
               if totalPhonemeCount !=0:
                   percentOfTotal = float(countingDict.get(item))/totalPhonemeCount
                   percentageDict[item] = (math.ceil((percentOfTotal*100)*100)/100)
               else:
                   percentageDict[item] = 0

       return percentageDict

    def phonemeFrequencyOutputter(self):

        consistentOrderList = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
       'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
       'UH','UW','V','W','Y','Z','ZH']

        transcriber = Transcriber()

        with open("phonemefreq/masterData.txt", 'w') as result:

           result.write(' '+',')
           for item in consistentOrderList:
               result.write(item + ',')
           result.write('\n')

           play_code_list = transcriber.get_play_code_list()
           for play in play_code_list:
               character_list = transcriber.get_character_list(play)
               for character in character_list:
                   filename = play+"_"+character

                   result.write(play+','+character + ',')
                   #print(filename,end='')

                   phonemeFreq = self.phoneme_frequency(filename)
                   for item in consistentOrderList:
                       result.write(str(phonemeFreq[item])+',')
                       #print(str(phonemeFreq[item]), end= ',')

                   #print('\n')
                   result.write('\n')


    def consonant_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of consonants
        '''

        text = read_file.read().split()

        self.global_consonants = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
            'stop':0, 'glottal':0, 'linguaalveolar':0, 'linguapalatal':0,
            'labiodental':0, 'bilabial':0, 'linguavelar':0,'linguadental':0,
            'voiced':0, 'voiceless':0, 'sibilant':0, 'nonsibilant':0,
            'sonorant':0, 'nonsonorant':0, 'coronal':0, 'noncoronal':0}
        self.consonant_count = 0

        for phoneme in text:
            if phoneme in self.consonant_classifier_dictionary:
                self.consonant_count +=1
                characteristics = self.consonant_classifier_dictionary[phoneme]
                for characteristic in characteristics:
                    self.global_consonants[characteristic]+=1

        return self.global_consonants, self.consonant_count

    def consonant_percentages(self, consonant_dictionary, consonant_count):
        '''
        Given a dictionary containing
        '''
        percentage_dict = {}
        for item in consonant_dictionary:
           if consonant_dictionary.get(item)!= None:
               if consonant_count !=0:
                   percent_of_total = float(consonant_dictionary.get(item))/consonant_count
                   percentage_dict[item] = (math.ceil((percent_of_total*100)*100)/100)
               else:
                   percentage_dict[item] = 0
        return percentage_dict

    def print_cons_percents(self, percentage_dict, read_file):
        fn = read_file.rstrip('.txt').lstrip('dest')
        with open("percents/{}_consonants_percents.csv".format(fn),'w') as result:
            result.write('feature , percent \n')
            for item in percentage_dict:
                result.write(item+" , "+str(percentage_dict[item])+"\n")


    def vowel_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of vowels
        '''

        text = read_file.read().split()

        self.global_vowels = {'monophthong':0, 'diphthong':0, 'central':0, 'front':0, 'back':0,
            'tense':0, 'lax':0, 'rounded':0,'unrounded':0}
        self.vowel_count = 0

        for phoneme in text:
            phoneme = phoneme[:-1]
            if phoneme in self.vowel_classifier_dictionary:
                self.vowel_count += 1
                characteristics = self.vowel_classifier_dictionary[phoneme]
                for characteristic in characteristics:
                    self.global_vowels[characteristic] +=1

        return self.global_vowels, self.vowel_count

    def vowel_percentages(self, vowel_dictionary, vowel_count):
        percentage_dict = {}
        for item in vowel_dictionary:
           if vowel_dictionary.get(item)!= None:
               if vowel_count != 0:
                   percent_of_total = float(vowel_dictionary.get(item))/vowel_count
                   percentage_dict[item] = (math.ceil((percent_of_total*100)*100)/100)
               else:
                   percentage_dict[item] = 0
        return percentage_dict

    def print_vowel_percents(self, percentage_dict, read_file):
        fn = read_file.rstrip('.txt').lstrip('/dest')
        with open("percents/{}_vowels_percents.csv".format(fn),'w') as result:
            result.write('feature , percent \n')
            for item in percentage_dict:
                result.write(item+" , "+str(percentage_dict[item])+"\n")


    def count_text(self, read_file):
        with open("dest/{}.txt".format(read_file), 'r') as source:
            with open("counts/{}_vowels.csv".format(read_file), 'w') as result:
                result.write("feature , count \n")
                vowel_count_dict = self.vowel_counts(source)[0]
                for item in vowel_count_dict:
                    result.write(item+" , "+str(vowel_count_dict[item])+"\n")
        with open("dest/{}.txt".format(read_file), 'r') as source:
            with open("counts/{}_consonants.csv".format(read_file), 'w') as result:
                result.write("feature , count \n")
                consonant_count_dict = self.consonant_counts(source)[0]
                for item in consonant_count_dict:
                    result.write(item+" , "+str(consonant_count_dict[item])+"\n")

    def percent_text(self, read_file):
        with open("dest/{}.txt".format(read_file), 'r') as source:
            cons_counts = self.consonant_counts(source)
            cons_pct_dict = self.consonant_percentages(cons_counts[0], cons_counts[1])
            self.print_cons_percents(cons_pct_dict, read_file)
        with open("dest/{}.txt".format(read_file), 'r') as source:
            vow_counts = self.vowel_counts(source)
            vow_pct_dict = self.vowel_percentages(vow_counts[0], vow_counts[1])
            self.print_vowel_percents(vow_pct_dict, read_file)


    def count_all_texts(self):
        '''
        For every file in the phonetic transcription folder, writes the counts of
        features to a new file in a counts folder. Entries are separated by newlines
        '''
        transcriber = Transcriber()
        play_code_list = transcriber.get_play_code_list()
        for play in play_code_list:
            character_list = transcriber.get_character_list(play)
            for character in character_list:
                filename = play+"_"+character
                self.count_text(filename)
                self.percent_text(filename)



def main():
    counter = Tagger()
    counter.count_all_texts()
    counter.phonemeFrequencyOutputter()


if __name__ == "__main__":
    main()
