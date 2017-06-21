import math
import os

'''
text_classifier.py
@authors Estelle Bayer, Liz Nichols, Summer 2017
A program that, given an ARPAbet source file, produces files containing information
about the raw number and percentage of a handful of linguistic features, separated
into vowel and consonant
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
        Given a dictionary of features and their counts as well as the overall
        number of consonants in a file, converts them to a percentage dictionary
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
        '''
        Given a dictionary of features and their percentages for a given file,
        prints those features to a new csv file
        '''
        fn = read_file.lstrip('/dest')
        with open("percents/consonants/{}_consonants_percents.csv".format(fn),'w') as result:
            result.write('feature,percent\n')
            for item in percentage_dict:
                result.write(item+","+str(percentage_dict[item])+"\n")


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
        '''
        Given a dictionary of features and their counts as well as the overall
        number of vowels in a file, converts them to a percentage dictionary
        '''
        percentage_dict = {}
        monophthong_count = vowel_dictionary['monophthong']
        diphthong = vowel_count - monophthong_count
        for item in vowel_dictionary:
            if vowel_dictionary.get(item)!= None and item != 'diphthong' and item != 'monophthong':
                if monophthong_count != 0:
                    percent_of_total = float(vowel_dictionary.get(item))/monophthong_count
                    percentage_dict[item] = (math.ceil((percent_of_total*100)*100)/100)
                else:
                    percentage_dict[item] = 0
            elif vowel_dictionary.get(item) != None:
                if vowel_count != 0:
                    percent_of_total = float(vowel_dictionary.get(item))/vowel_count
                    percentage_dict[item] = (math.ceil((percent_of_total*100)*100)/100)
                else:
                    percentage_dict[item] = 0
        return percentage_dict

    def print_vowel_percents(self, percentage_dict, read_file):
        '''
        Given a dictionary of features and their percentages for a given file,
        prints those features to a new csv file
        '''
        fn = read_file.lstrip('/dest')
        with open("percents/vowels/{}_vowels_percents.csv".format(fn),'w') as result:
            result.write('feature,percent\n')
            for item in percentage_dict:
                result.write(item+","+str(percentage_dict[item])+"\n")


    def count_text(self, read_file):
        '''
        Given a text file name, writes the counts of its consonant and vowel features
        to two new csv files in the percents folder
        '''
        with open("dest/{}.txt".format(read_file), 'r') as source:
            with open("counts/{}_vowels.csv".format(read_file), 'w') as result:
                result.write("feature,count\n")
                vowel_count_dict = self.vowel_counts(source)[0]
                for item in vowel_count_dict:
                    result.write(item+","+str(vowel_count_dict[item])+"\n")
        with open("dest/{}.txt".format(read_file), 'r') as source:
            with open("counts/{}_consonants.csv".format(read_file), 'w') as result:
                result.write("feature,count\n")
                consonant_count_dict = self.consonant_counts(source)[0]
                for item in consonant_count_dict:
                    result.write(item+","+str(consonant_count_dict[item])+"\n")

    def percent_text(self, read_file):
        '''
        Given a file, writes the percentages of its consonant and vowel features
        to two new csv files in the percents folder
        '''
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
        features to a two new csv files in a counts folder
        '''

        for filename in os.listdir("dest/"):
            file_base = filename[:-4]
            self.count_text(file_base)
            self.percent_text(file_base)



def main():
    counter = Tagger()
    counter.count_all_texts()

if __name__ == "__main__":
    main()
