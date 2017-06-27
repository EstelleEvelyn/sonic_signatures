import numpy
from sklearn.naive_bayes import GaussianNB
import csv
import re
import sys
import random

'''
naive_bayes.py
Estelle Bayer, Summer 2017
A program to classify Shakespearean characters based on the phonetic features of
their speech
'''
def get_fit(play, trait, data):
    fit_set = []
    trait_indeces = {'gender':1, 'role':2, 'genre':3}
    class_list = {'f':0, 'm':1, 'protag':2, 'antag':3, 'other':4, 'comedy':5, 'tragedy':6, 'history':7}

    with open('characteristics.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if re.match(play+"_", row[0]):
                fit_set.append(class_list[row[trait_indeces[trait]]])
    return fit_set

def get_new_data(play, data_file):
    #get some new data
    new_data = []
    with open(data_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if re.match(play, row[0]):
                new_data.append(list(map(lambda x: float(x), (row[1:]))))
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
    elif data[0].lower() == 'f':
        data_file = "../tagging/features/percentData.csv"
    else:
        print("Invalid data type. Please enter \"[p]honeme\" or \"[f]eature\"")
        sys.exit() #TODO prompt for input instead

    training_choices = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4',
                            'H5', '1H6', '2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac',
                            'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
                            'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']
    training_choices.remove(play_code)

    # random_training = random.randint(0,37)
    # training_play = training_choices[random_training]

    training_data = []
    fit = []

    for training_play in training_choices:
        play_fit = get_fit(training_play, trait, data)
        fit.append(play_fit)
        with open(data_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if re.match(training_play+"_", row[0]):
                    training_data.append(list(map(lambda x: float(x), (row[1:]))))

    training_data = numpy.array(training_data)
    fit = numpy.array(sum(fit, []))


    gnb = GaussianNB()
    gnb.fit(training_data, fit)

    predict_data = get_new_data(play_code, data_file)
    print("Predicted:", gnb.predict(predict_data))
    print("Actual:", numpy.array(get_fit(play_code, trait, data)))

if __name__ == "__main__":
    main()
