import csv
import os

'''
csv_separator.py
@author Estelle Bayer, Summer 2017
A program designed to separate consonant percentage files into manner, voice,
and articulation for use with a pie chart modeler
'''
class MPV:
    def __init__(self, read_file):
        self.file_base = read_file[:-24]
        self.read_file = read_file
        self.reader = {}


    def get_manner(self):
        with open("percents/consonants/{}".format(self.read_file)) as csvfile:
            self.reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            with open("features/{}_manner.csv".format(self.file_base), 'w') as result:
                result.write("feature,percent\n")
                for row in self.reader:
                    if row.get('feature') in ['stop', 'affricate', 'fricative', 'liquid', 'glide', 'nasal']:
                        result.write(row.get('feature')+","+row.get('percent')+"\n")

    def get_placement(self):
        with open("percents/consonants/{}".format(self.read_file)) as csvfile:
            self.reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            with open("features/{}_placement.csv".format(self.file_base), 'w') as result:
                result.write("feature,percent\n")
                for row in self.reader:
                    if row.get('feature') in ['bilabial', 'linguaalveolar', 'linguadental', 'labiodental', 'linguavelar', 'glottal', 'linguapalatal']:
                        result.write(row.get('feature')+","+row.get('percent')+"\n")

    def get_voicing(self):
        with open("percents/consonants/{}".format(self.read_file)) as csvfile:
            self.reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            with open("features/{}_voicing.csv".format(self.file_base), 'w') as result:
                result.write("feature,percent\n")
                for row in self.reader:
                    if row.get('feature') in ['voiced', 'voiceless']:
                        result.write(row.get('feature')+","+row.get('percent')+"\n")

    def separate_file(self):
        self.get_manner()
        self.get_placement()
        self.get_voicing()

def main():
    for filename in os.listdir("percents/consonants"):
        separator = MPV(filename)
        separator.separate_file()

if __name__ == "__main__":
    main()
