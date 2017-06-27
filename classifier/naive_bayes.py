import numpy
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from scipy.spatial.distance import hamming
import csv
import re
import sys
import statistics
import random

'''
naive_bayes.py
Estelle Bayer, Summer 2017
A program to classify Shakespearean characters based on the phonetic features of
their speech using Gaussian or multinomial naive Bayes classifiers, with multiple
class designation options
'''

GLOBAL_PLAY_LIST = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4',
                        'H5', '1H6', '2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac',
                        'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
                        'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']

def get_training_data(training_play, data_file):
    training = []
    with open(data_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if re.match(training_play+"_", row[0]):
                training.append(list(map(lambda x: float(x), (row[1:]))))
    return training

def get_fit(play, trait):
    fit_set = []
    trait_indeces = {'gender':1, 'role':2, 'genre':3}
    class_list = {'f':0, 'm':1, 'protag':2, 'antag':3, 'other':4, 'comedy':5, 'tragedy':6, 'history':7}

    # #this is highly inaccurate.
    # class_list = {('f', 'protag', 'comedy'):0, ('f', 'protag', 'tragedy'):1, ('f', 'protag', 'history'):2,
    #              ('f', 'antag', 'comedy'):3, ('f', 'antag', 'tragedy'):4, ('f', 'antag', 'history'):5,
    #              ('f', 'other', 'comedy'):6, ('f', 'other', 'tragedy'):7, ('f', 'other', 'history'):8,
    #              ('m', 'protag', 'comedy'):9, ('m', 'protag', 'tragedy'):10, ('m', 'protag', 'history'):11,
    #              ('m', 'antag', 'comedy'):12, ('m', 'antag', 'tragedy'):13, ('m', 'antag', 'history'):14,
    #              ('m', 'other', 'comedy'):15, ('m', 'other', 'tragedy'):16, ('m', 'other', 'history'):17}

    with open('characteristics.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if re.match(play+"_", row[0]):
                fit_set.append(class_list[row[trait_indeces[trait]]])
                # fit_set.append(class_list[(row[1], row[2], row[3])])
    return fit_set

def get_new_data(play, data_file):
    #get some new data
    new_data = []
    with open(data_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if re.match(play+"_", row[0]):
                new_data.append(list(map(lambda x: float(x), (row[1:]))))
    return numpy.array(new_data)

def predict_data(play, trait, data_file):

        training_choices = GLOBAL_PLAY_LIST.copy()
        training_choices.remove(play)

        # random_training = random.randint(0,37)
        # training_play = training_choices[random_training]

        training_data = []
        fit = []

        for training_play in training_choices:
            play_fit = get_fit(training_play, trait)
            fit.append(play_fit)
            play_data = get_training_data(training_play, data_file)
            training_data.append(play_data)


        training_data = numpy.array(sum(training_data, []))
        fit = numpy.array(sum(fit, []))


        # gnb = GaussianNB()
        # gnb.fit(training_data, fit)
        mnb  = MultinomialNB()
        mnb.fit(training_data, fit)

        predict_data = get_new_data(play, data_file)
        predicted = mnb.predict(predict_data)
        # predicted = gnb.predict(predict_data)
        actual = numpy.array(get_fit(play, trait))

        return predicted, actual


def main():
    if len(sys.argv) < 4:
        print("Usage: naive_bayes.py <play_code> <characteristic> <[p]honeme or [f]eature>")
        sys.exit()
    else:
        play_code = sys.argv[1]
        trait = sys.argv[2]
        data = sys.argv[3]

    if data[0].lower() == 'p':
        data_file = "../tagging/phonemefreq/masterData.csv"
    elif data[0].lower() == 'f':
        data_file = "../tagging/features/percentData.csv"
    else:
        print("Invalid data type. Please enter \"[p]honeme\" or \"[f]eature\"")
        sys.exit() #TODO prompt for input instead

    hamm_dist = []
    for play in GLOBAL_PLAY_LIST:
        predicted, actual = predict_data(play, trait, data_file)
        hamm_dist.append(hamming(predicted, actual))
    print(statistics.mean(hamm_dist))
    # print("Predicted:", gnb.predict(predict_data))
    # print("Actual:", numpy.array(get_fit(play_code, trait))

if __name__ == "__main__":
    main()
