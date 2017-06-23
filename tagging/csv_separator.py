import csv
import os

'''
csv_separator.py
@author Estelle Bayer, Summer 2017
A program designed to separate consonant percentage files into manner, voice,
and articulation for use with a pie chart modeler
'''
class MPV:
    def get_manner(self):
        key_list = ['stop', 'affricate', 'fricative', 'liquid', 'glide', 'nasal']
        with open("percentData.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open('mannerData.csv', 'w') as result:
                result.write("filename,stop,affricate,fricative,liquid,glide,nasal\n")
                for row in reader:
                    result.write(row.get('filename'))
                    for key in key_list:
                        result.write(','+row.get(key))
                    result.write('\n')

    def get_placement(self):
        key_list = ['bilabial', 'linguaalveolar', 'linguadental', 'labiodental', 'linguavelar', 'glottal', 'linguapalatal']
        with open('percentData.csv', 'r') as csvfile:
            reader = csv.DictReader(x.replace(csvfile))
            with open("placementData.csv", 'w') as result:
                result.write("filename,bilabilal,linguaalveolar,linguadental,labiodental,linguavelar,glottal,linguapalatal\n")
                for row in reader:
                    result.write(row.get('filename'))
                    for key in key_list:
                        result.write(','+row.get(key))
                    result.write("\n")

    def get_voicing(self):
        with open('percentData.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open("voicingData.csv", 'w') as result:
                result.write("filename,voiced,voiceless\n")
                for row in reader:
                    result.write(row.get('filename')+","+row.get('voiced')+row.get('voiceless')+"\n")
                result.write('\n')


    def separate_file(self):
        self.get_manner()
        self.get_placement()
        self.get_voicing()

def main():
    separator = MPV()
    separator.separate_file()

if __name__ == "__main__":
    main()
