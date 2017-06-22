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
            for row in file_reader:
                if not row.get('feature') in self.feature_dict:
                    self.feature_dict[row.get('feature')] = [float(row.get('percent'))]
                else:
                    self.feature_dict[row.get('feature')].append(float(row.get('percent')))

    def calc_stats(self):
        for filename in os.listdir("../tagging/percents/consonants"):
            self.accumulate("../tagging/percents/consonants/{}".format(filename))
        for filename in os.listdir("../tagging/percents/vowels"):
            self.accumulate("../tagging/percents/vowels/{}".format(filename))
        with open('feature_statistics.txt', 'w') as out_file:
            out_file.write('feature,stdev,variance\n')
            for feature in self.feature_dict:
                feature_std_dev = statistics.stdev(self.feature_dict[feature])
                feature_var = statistics.variance(self.feature_dict[feature])
                out_file.write(feature+","+str(feature_std_dev)+","+str(feature_var)+"\n")
        # with open('phoneme_statistics.txt', 'w') as out_file:
        #     out_file.write('phoneme,stdev,variance')
        #     for phoneme in self.phoneme_dict:
        #         phoneme_std_dev = statistics.stdev(self.phoneme_dict[phoneme])
        #         phoneme_var = statistics.variance(self.phoneme_dict[phoneme])
        #         out_file.write(phoneme+","+phoneme_std_dev+","+phoneme_var)

def main():
    stats = Stat_counter()
    stats.calc_stats()

if __name__ == "__main__":
    main()
