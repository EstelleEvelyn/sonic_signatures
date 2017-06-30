import statistics
import csv
import os
'''
calc_stats.py
Estelle Bayer, Summer 2017
A program to calculate the standard deviations and variances of various features
and phonemes in Shakespearean text files
'''

class StatCounter:
    def __init__(self):
        self.feature_dict = {'fricative':[], 'affricate':[], 'glide':[], 'nasal':[],
                    'liquid':[],'stop':[], 'glottal':[], 'linguaalveolar':[],
                    'linguapalatal':[], 'labiodental':[], 'bilabial':[],'linguavelar':[],
                    'linguadental':[], 'voiced':[], 'voiceless':[], 'sibilant':[],
                    'nonsibilant':[],'sonorant':[], 'nonsonorant':[], 'coronal':[],
                    'noncoronal':[], 'monophthong':[], 'diphthong':[], 'central':[],
                    'front':[], 'back':[], 'tense':[], 'lax':[], 'rounded':[],'unrounded':[]}
        self.phoneme_dict = {'AA':[], 'AE':[], 'AH':[], 'AO':[], 'AW':[], 'AY':[],
            'B':[], 'CH':[], 'D':[], 'DH':[], 'EH':[], 'ER':[], 'EY':[], 'F':[],
            'G':[], 'HH':[], 'IH':[], 'IY':[], 'JH':[], 'K':[], 'L':[], 'M':[],
            'N':[], 'NG':[], 'OW':[], 'OY':[], 'P':[], 'R':[], 'S':[], 'SH':[], 'T':[],
            'TH':[], 'UH':[], 'UW':[], 'V':[], 'W':[], 'Y':[], 'Z':[], 'ZH':[]}
        self.threshold = 500
        self.files_used= 0

    def accumuate_phonemes(self):
        '''
        Based on previously calculated phoneme distributions for every character,
        returns a dictionary containing phonemes as keys and lists of percentages
        for every phoneme as values
        e.g. {'AA':[.021, .03, .0128,...], 'AH':[...], ...}
        '''
        order_list = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
            'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S',
            'SH','T','TH', 'UH','UW','V','W','Y','Z','ZH']
        with open("../tagging/phonemefreq/masterData.csv") as csvfile:
            file_reader = csv.reader(csvfile)
            for row in file_reader:
                with open("../tagging/phonemefreq/masterCounts.csv") as checkfile:
                    checker = csv.reader(checkfile)
                    for char in checker:
                        if char[0] == row[0] != 'filename' and sum(map(lambda x: int(x),
                            char[1:])) > self.threshold:
                            self.files_used += 1
                            for i in range(len(order_list)):
                                self.phoneme_dict[order_list[i]].append(float(row[i+1]))


    def accumulate_features(self):
        '''
        Based on previously calculated feature distributions for every character,
        returns a dictionary containing features as keys and lists of percentages
        for those features as values
        e.g. {'front':[.378, .4022, .367,...], 'fricative':[...], ...}
        '''
        order_list  =['fricative', 'affricate', 'glide', 'nasal', 'liquid',
            'stop', 'glottal', 'linguaalveolar', 'linguapalatal', 'labiodental',
            'bilabial', 'linguavelar','linguadental', 'voiced', 'voiceless',
            'sibilant', 'nonsibilant', 'sonorant', 'nonsonorant', 'coronal',
            'noncoronal', 'monophthong', 'diphthong', 'central', 'front', 'back',
            'tense', 'lax', 'rounded','unrounded']

        with open("../tagging/features/percentData.csv") as csvfile:
            file_reader = csv.reader(csvfile)
            for row in file_reader:
                with open("../tagging/phonemefreq/masterCounts.csv") as checkfile:
                    checker = csv.reader(checkfile)
                    for char in checker:
                        if char[0] == row[0] != 'filename' and sum(map(lambda x: int(x),
                            char[1:])) > self.threshold:
                            for i in range(len(order_list)):
                                self.feature_dict[order_list[i]].append(float(row[i+1]))

    def calc_stats(self):
        '''
        Calculates the standard deviation and variance of every feature and every
        phoneme, printing the data for every feature to feature_statistics.csv
        and the data for every phoneme to phoneme_statistics.csv
        '''
        self.accumuate_phonemes()
        self.accumulate_features()

        with open('feature_statistics.csv', 'w') as out_file:
            out_file.write('feature,mean,stdev,variance\n')
            for feature in self.feature_dict:
                feature_mean = statistics.mean(self.feature_dict[feature])
                feature_std_dev = statistics.stdev(self.feature_dict[feature])
                feature_var = statistics.variance(self.feature_dict[feature])
                out_file.write(feature+","+str(feature_mean)+","+str(feature_std_dev)+","+str(feature_var)+"\n")
        with open('phoneme_statistics.csv', 'w') as out_file:
            out_file.write('phoneme,mean,stdev,variance\n')
            for phoneme in self.phoneme_dict:
                phoneme_mean = statistics.mean(self.phoneme_dict[phoneme])
                phoneme_std_dev = statistics.stdev(self.phoneme_dict[phoneme])
                phoneme_var = statistics.variance(self.phoneme_dict[phoneme])
                out_file.write(phoneme+","+str(phoneme_mean)+","+str(phoneme_std_dev)+","+str(phoneme_var)+"\n")

def main():
    stats = StatCounter()
    stats.calc_stats()
    # print(stats.files_used)

if __name__ == "__main__":
    main()
