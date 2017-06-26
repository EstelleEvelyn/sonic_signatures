import numpy
from sklearn.naive_bayes import GaussianNB
import csv
import re
import sys

'''
naive_bayes.py
Estelle Bayer, Summer 2017
A program to classify Shakespearean characters based on the phonetic features of
their speech
'''
def get_training_fit(dataset):
    #cross-reference some known quantity of traits
    fit_set = []
    with open('characteristics.csv', 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if row.get('character') in dataset:
                for item in row:
                    if item != 'character':
                        fit_set.append((item, row[item]))
    return numpy.array(fit_set)

def get_new_data():
    #get some new data
    new_data = []
    with open("../tagging/features/percentData.csv", 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if re.match('AYL_', row.get('filename')):
                new_data.append(row)
    return numpy.array(new_data)

def main():

    if len(sys.argv) < 4:
        print("Usage: naive_bayes.py <play_code> <characteristic> <[p]honeme or [f]eature>")
        sys.exit()
    else:
        play_code = sys.argv[1]
        trait = sys.argv[2]
        data = sys.argv[3]


    feature_order_list = ['linguaalveolar', 'monophthong', 'rounded', 'affricate',
                'nonsonorant', 'liquid', 'sonorant', 'nasal', 'back', 'labiodental',
                'linguapalatal', 'linguavelar', 'coronal', 'tense', 'bilabial',
                'front', 'unrounded', 'stop', 'central', 'glide', 'fricative',
                'voiceless', 'glottal','voiced', 'sibilant', 'nonsibilant',
                'diphthong', 'lax', 'noncoronal', 'linguadental']
    phoneme_order_list = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
               'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
               'UH','UW','V','W','Y','Z','ZH']

    if data[0].lower() == 'p':
        data_file = "../tagging/phonemefreq/masterData.csv"
    elif data[1].lower() == 'f':
        data_file = "../tagging/features/percentData.csv"
    else:
        print("Invalid data type. Please enter \"[p]honeme\" or \"[f]eature\"")
        sys.exit() #TODO prompt for input instead

    training_data = []
    with open(data_file, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if re.match(play_code+'_', row.get('filename')):
                training_data.append(row)
    training_data = numpy.array(training_data)
    gnb = GaussianNB()
    fit = get_training_fit(training_data)
    gnb.fit(training_data, fit)

    predict_data = get_new_data()
    print(gnb.predict(predict_data))

if __name__ == "__main__":
    main()
