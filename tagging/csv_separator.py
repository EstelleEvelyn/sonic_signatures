import csv
import os

'''
csv_separator.py
@author Estelle Bayer, Summer 2017
A program designed to separate feature percentage data into manner, voice,
and articulation
Possibly obsolete/redundant after csv implementation
'''

class MPV:
    def get_manner(self):
        '''
        Extracts the features related to manner from the csv file containing
        information about every feature and writes them to a separate file
        '''
        key_list = ['stop', 'affricate', 'fricative', 'liquid', 'glide', 'nasal']
        with open("features/percentData.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open('features/mannerData.csv', 'w') as result:
                result.write("filename,stop,affricate,fricative,liquid,glide,nasal\n")
                for row in reader:
                    result.write(row.get('filename'))
                    for key in key_list:
                        result.write(','+row.get(key))
                    result.write('\n')

    def get_placement(self):
        '''
        Extracts the features related to placement from the csv file containing
        information about every feature and writes them to a separate file
        '''
        key_list = ['bilabial', 'linguaalveolar', 'linguadental', 'labiodental', 'linguavelar', 'glottal', 'linguapalatal']
        with open('features/percentData.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open("features/placementData.csv", 'w') as result:
                result.write("filename,bilabilal,linguaalveolar,linguadental,labiodental,linguavelar,glottal,linguapalatal\n")
                for row in reader:
                    result.write(row.get('filename'))
                    for key in key_list:
                        result.write(','+row.get(key))
                    result.write("\n")

    def get_voicing(self):
        '''
        Extracts the features related to voicing from the csv file containing
        information about every feature and writes them to a separate file
        '''
        with open('features/percentData.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            with open("features/voicingData.csv", 'w') as result:
                result.write("filename,voiced,voiceless\n")
                for row in reader:
                    result.write(row.get('filename')+","+row.get('voiced')+row.get('voiceless')+"\n")
                result.write('\n')


    def separate_file(self):
        '''
        Separates manner, placement, and voicing features into their own csv files
        '''
        self.get_manner()
        self.get_placement()
        self.get_voicing()

def main():
    separator = MPV()
    separator.separate_file()

if __name__ == "__main__":
    main()
