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

    def accumulate(self, read_file):
        with open(read_file, 'r') as csvfile:
            file_reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            for line in file_reader:
                if not row.get('feature') in self.feature_dict:
                    self.feature_dict[row.get('feature')] = [row.get('percent')]
                else:
                    self.feature_dict[row.get('feature')].append(row.get('percent'))

    def calc_stats(self, read_file):
        self.accumulate(read_file)
        with open('feature_statistics.txt', 'w') as out_file:
            out_file.write('feature,stdev,variance')
            for feature in self.feature_dict:
                feature_std_dev = statistics.stdev(self.feature_dict[feature])
                feature_var = statistics.variance(self.feature_dict[feature])
                out_file.write(feature+","+feature_std_dev+","+feature_var)
        # with open('phoneme_statistics.txt', 'w') as out_file:
        #     out_file.write('phoneme,stdev,variance')
        #     for phoneme in self.phoneme_dict:
        #         phoneme_std_dev = statistics.stdev(self.phoneme_dict[phoneme])
        #         phoneme_var = statistics.variance(self.phoneme_dict[phoneme])
        #         out_file.write(phoneme+","+phoneme_std_dev+","+phoneme_var)

def main():
    stats = Stat_counter()
    for filename in os.listdir("../tagging/percents/consonants"):
        stats.calc_stats(filename)
    for filename in os.listdir("../tagging/percents/vowels"):
        stats.calc_stats(filename)

if __name__ == "__main__":
    main()
