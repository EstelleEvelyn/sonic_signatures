import statistics
import csv
import os
'''
calc_stats.py
Estelle Bayer, Summer 2017
A program to calculate the standard deviations and variances of various features
and phonemes in Shakespearean text files
'''

class Stat_counter:
    def __init__(self):
        self.feature_dict = {}
        self.phoneme_dict = {}

    def accumuate_phonemes(self):
        with open("../tagging/phonemefreq/masterData_combined.csv") as csvfile:
            file_reader = csv.DictReader(csvfile)
            for row in file_reader:
                for phoneme in row:
                    if(phoneme != ''):
                        if not phoneme in self.phoneme_dict:
                            self.phoneme_dict[phoneme]=[float(row.get(phoneme))]
                        else:
                            self.phoneme_dict[phoneme].append(float(row.get(phoneme)))


    def accumulate_features(self):
        with open("../tagging/features/percentData.csv") as csvfile:
            file_reader = csv.DictReader(csvfile)
            for row in file_reader:
                for feature in row:
                    if (feature != 'filename'):
                        if not feature in self.feature_dict:
                            self.feature_dict[feature] = [float(row.get(feature))]
                        else:
                            self.feature_dict[feature].append(float(row.get(feature)))

    def calc_stats(self):
        self.accumuate_phonemes()
        self.accumulate_features()

        with open('feature_statistics.txt', 'w') as out_file:
            out_file.write('feature,stdev,variance\n')
            for feature in self.feature_dict:
                feature_std_dev = statistics.stdev(self.feature_dict[feature])
                feature_var = statistics.variance(self.feature_dict[feature])
                out_file.write(feature+","+str(feature_std_dev)+","+str(feature_var)+"\n")
        with open('phoneme_statistics.txt', 'w') as out_file:
            out_file.write('phoneme,stdev,variance\n')
            for phoneme in self.phoneme_dict:
                phoneme_std_dev = statistics.stdev(self.phoneme_dict[phoneme])
                phoneme_var = statistics.variance(self.phoneme_dict[phoneme])
                out_file.write(phoneme+","+str(phoneme_std_dev)+","+str(phoneme_var)+"\n")

def main():
    stats = Stat_counter()
    stats.calc_stats()

if __name__ == "__main__":
    main()
