import math
import os
import csv
from operator import itemgetter

'''
feature_counter.py
@authors Estelle Bayer, Liz Nichols, Summer 2017
A program that generates csv files enumerating the phonemic and feature frequencies
for all ARPAbet source files
'''

class Counter:
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

        self.feature_ordered_list = ['fricative', 'affricate', 'glide', 'nasal', 'liquid',
            'stop', 'glottal', 'linguaalveolar', 'linguapalatal', 'labiodental', 'bilabial',
            'linguavelar','linguadental', 'voiced', 'voiceless', 'sibilant', 'nonsibilant',
            'sonorant', 'nonsonorant', 'coronal', 'noncoronal', 'monophthong', 'diphthong',
            'central', 'front', 'back', 'tense', 'lax', 'rounded','unrounded']

    def get_features(self):
        return(global_consonants.keys().append(global_vowels.keys()))

    def phoneme_frequency(self, read_file):
        ''' most of the research on phonemes in speech comes not from the distinctive
        features of phonemes used but from the phonemes themselves - counts the number of
        each phoneme and assesses the frequencies of each'''

        counting_dict = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
        'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
        'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
        'DH':0,'D':0,'CH':0}
        percentage_dict = {}

        total_phoneme_count = 0

        with open("dest/{}.txt".format(read_file), 'r') as source:
            text = source.read().split()
            for phoneme in text:
                if phoneme[-1] in '0123456789':
                    phoneme = phoneme[:-1]
                if phoneme in counting_dict:
                    total_phoneme_count +=1
                if phoneme in counting_dict:
                    counting_dict[phoneme]+=1

        for item in counting_dict:
            if counting_dict.get(item)!= None:
                if total_phoneme_count !=0:
                    percent_of_total = float(counting_dict.get(item))/total_phoneme_count
                    percentage_dict[item] = percent_of_total
                else:
                    percentage_dict[item] = 0

        return percentage_dict, counting_dict

    def phoneme_frequency_outputter(self):
        '''
        Calculates the percentage for every phoneme within every character's text
        and writes the information to a CSV file
        '''
        consistentOrderList = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
        'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
        'UH','UW','V','W','Y','Z','ZH']



        with open("phonemefreq/masterData.csv", 'w') as result:
            result.write('filename')
            for item in consistentOrderList:
                result.write(','+item)
            result.write('\n')

            presort_list = []
            for filename in os.listdir("dest"):
                temp_list = []
                filename = filename[:-4]
                # play, character = filename.split("_")
                # result.write(play+','+character + ',')
                temp_list.append(filename)
                #print(filename,end='')

                phonemeFreq = self.phoneme_frequency(filename)[0]
                for item in consistentOrderList:
                    temp_list.append(str(phonemeFreq[item]))
                #print(str(phonemeFreq[item]), end= ',')

                #print('\n')
                presort_list.append(temp_list)

            presort_list.sort(key = itemgetter(0))
            data = presort_list
            csv.writer(result).writerows(data)

    def phoneme_count_outputter(self):
        '''
        Calculates the percentage for every phoneme within every character's text
        and writes the information to a CSV file
        '''
        consistentOrderList = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
       'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
       'UH','UW','V','W','Y','Z','ZH']



        with open("phonemefreq/masterCounts.csv", 'w') as result:

            result.write('filename')
            for item in consistentOrderList:
               result.write(','+item)
            result.write('\n')

            presort_list = []
            for filename in os.listdir("dest"):
                temp_list = []
                filename = filename[:-4]
                # play, character = filename.split("_")
                # result.write(play+','+character + ',')
                temp_list.append(filename)
                #print(filename,end='')

                phonemeFreq = self.phoneme_frequency(filename)[1]
                for item in consistentOrderList:
                    temp_list.append(str(phonemeFreq[item]))
                   #print(str(phonemeFreq[item]), end= ',')

                #print('\n')
                presort_list.append(temp_list)

            presort_list.sort(key = itemgetter(0))
            data = presort_list
            csv.writer(result).writerows(data)


    def consonant_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of consonants and
        the total number of consonant phonemes encountered
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
        Given a dictionary containing the counts of various consonant features and
        the total number of consonants in the related file, calculates percentages
        for every tracked consonant feature
        '''
        percentage_dict = {}
        for item in consonant_dictionary:
            if consonant_dictionary.get(item)!= None:
                if consonant_count !=0:
                    percent_of_total = float(consonant_dictionary.get(item))/consonant_count
                    percentage_dict[item] = percent_of_total
                else:
                    percentage_dict[item] = 0
        return percentage_dict

    # def print_cons_percents(self, percentage_dict, read_file):
    '''
    A method which at one point wrote percentage information to a separate file
    for every character. Scrapped in favor of keeping percentage data in one csv
    '''
    #     fn = read_file.lstrip('dest')
    #     with open("percents/{}_consonants_percents.csv".format(fn),'w') as result:
    #         result.write('feature,percent\n')
    #         for item in percentage_dict:
    #             result.write(item+","+str(percentage_dict[item])+"\n")


    def vowel_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of vowels as well
        as the total number of vowels in the given file
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
        '''
        Given a dictionary containing the counts of various vowel features and
        the total number of consonants in the related file, calculates percentages
        for every tracked vowel feature
        '''
        percentage_dict = {}
        for item in vowel_dictionary:
            if vowel_dictionary.get(item)!= None:
                if vowel_count != 0:
                    percent_of_total = float(vowel_dictionary.get(item))/vowel_count
                    percentage_dict[item] = percent_of_total
                else:
                    percentage_dict[item] = 0
        return percentage_dict

    # def print_vowel_percents(self, percentage_dict, read_file):
        '''
        A method which at one point wrote percentage information to a separate file
        for every character. Scrapped in favor of keeping percentage data in one csv
        '''
    #     fn = read_file.lstrip('/dest')
    #     with open("percents/{}_vowels_percents.csv".format(fn),'w') as result:
    #         result.write('feature,percent\n')
    #         for item in percentage_dict:
    #             result.write(item+","+str(percentage_dict[item])+"\n")


    def count_text(self, read_file):
        '''
        Given a file, returns a dictionary whose keys are features and whose values
        are the tally count of that feature in the given file
        '''
        with open("dest/{}.txt".format(read_file), 'r') as source:
            vowel_count_dict = self.vowel_counts(source)[0]

        with open("dest/{}.txt".format(read_file), 'r') as source:
            consonant_count_dict = self.consonant_counts(source)[0]

        consonant_count_dict.update(vowel_count_dict)
        count_dict = consonant_count_dict
        return count_dict

    def percent_text(self, read_file):
        '''
        Given a file, returns a dictionary whose keys are features and whose values
        are the percentageof the given file that feature comprises
        '''
        with open("dest/{}.txt".format(read_file), 'r') as source:
            cons_counts = self.consonant_counts(source)
            cons_pct_dict = self.consonant_percentages(cons_counts[0], cons_counts[1])
        with open("dest/{}.txt".format(read_file), 'r') as source:
            vow_counts = self.vowel_counts(source)
            vow_pct_dict = self.vowel_percentages(vow_counts[0], vow_counts[1])

        cons_pct_dict.update(vow_pct_dict)
        pct_dict = cons_pct_dict
        return pct_dict

    def count_all_texts(self):
        '''
        Writes the counts of all the features of every file to its own line in a
        counts csv file and writes the percents of all the features of every file
        to its own line in  a percents csv file
        '''
        with open ('features/percentData.csv', 'w') as result:
            result.write('filename')
            for item in self.feature_ordered_list:
                result.write(','+item)
            result.write('\n')

            presort_list = []
            for filename in os.listdir("dest"):
                temp_list = []
                filename = filename[:-4]
                # play, character = filename.split("_")
                # result.write(play+','+character + ',')
                temp_list.append(filename)

                pct_dict = self.percent_text(filename)
                for item in self.feature_ordered_list:
                    temp_list.append(str(pct_dict[item]))

                presort_list.append(temp_list)

            presort_list.sort(key = itemgetter(0))
            data = presort_list
            csv.writer(result).writerows(data)


        with open ('features/countData.csv', 'w') as result:
            result.write('filename')
            for item in self.feature_ordered_list:
                result.write(','+item)
            result.write('\n')

            presort_list = []
            for filename in os.listdir("dest"):
                temp_list = []
                filename = filename[:-4]
                # play, character = filename.split("_")
                # result.write(play+','+character + ',')
                temp_list.append(filename)

                count_dict = self.count_text(filename)
                for item in self.feature_ordered_list:
                    temp_list.append(str(count_dict[item]))

                presort_list.append(temp_list)

            presort_list.sort(key = itemgetter(0))
            data = presort_list
            csv.writer(result).writerows(data)

            self.phoneme_frequency_outputter()
            self.phoneme_count_outputter()




def main():
    counter = Counter()
    counter.count_all_texts()


if __name__ == "__main__":
    main()
