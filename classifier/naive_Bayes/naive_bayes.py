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
class Naive_Bayes:
    def get_sample_weight(self, char):
        '''
        @param char: the character withheld
        @return weight_list: the size for a given role, used to weight the training sample
        '''
        weight_list = []
        with open('../../tagging/phonemefreq/masterCounts.csv', 'r') as weightfile:
            reader = csv.reader(weightfile)
            for row in reader:
                if row[0] != 'filename' and row[0] != char:
                    size = sum(list(map(lambda x: float(x), row[1:])))
                    weight_list.append(size)
        return numpy.array(weight_list)

    def get_training_data_play(self, training_play, data_file):
        '''
        @param training_play: a string play code in the training data
        @param data_file: a string of either the phoneme percent or feature percent file,
            based on command line input
        @return training: a list of the percent distributions for every character in the
            training play. used to train the naive Bayes classifier
        '''
        training = []
        with open(data_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if re.match(training_play+"_", row[0]):
                    training.append(list(map(lambda x: float(x), row[1:])))
        return training

    def get_training_data_char(self, char, data_file):
        '''
        @param char: the string char being withheld
        @return training: a list of nasal feature percent for every character other than
            the withheld char
        @return withheld: the nasal feature percent for the withheld character
        '''
        training = []
        withheld = []
        with open(data_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if char != row[0] and row[0] != 'filename':
                    training.append(list(map(lambda x: float(x), row[1:])))
                elif char == row[0] and row[0] != 'filename':
                    withheld.append(list(map(lambda x: float(x), row[1:])))
        return numpy.array(withheld), numpy.array(training)

    def get_fit(self, target, trait):
        '''
        @param target: a string of either a play or character for which we want to obtain
            the value(s) of the specified trait
        @param trait: "gender", "role", or "genre". The class on which the classifier
            is deciding, specified in arguments to main
        @return fit_set: a list containing the correct classification(s) for the
            target character(s)
        '''
        fit_set = []
        trait_indeces = {'gender':1, 'role':2, 'genre':3}
        class_list = {'f':0, 'm':1, 'protag':2, 'antag':3, 'fool':4, 'other':5, 'comedy':6, 'tragedy':7, 'history':8}

        # #this is highly inaccurate.
        # class_list = {('f', 'protag', 'comedy'):0, ('f', 'protag', 'tragedy'):1, ('f', 'protag', 'history'):2,
        #              ('f', 'antag', 'comedy'):3, ('f', 'antag', 'tragedy'):4, ('f', 'antag', 'history'):5,
        #              ('f', 'other', 'comedy'):6, ('f', 'other', 'tragedy'):7, ('f', 'other', 'history'):8,
        #              ('m', 'protag', 'comedy'):9, ('m', 'protag', 'tragedy'):10, ('m', 'protag', 'history'):11,
        #              ('m', 'antag', 'comedy'):12, ('m', 'antag', 'tragedy'):13, ('m', 'antag', 'history'):14,
        #              ('m', 'other', 'comedy'):15, ('m', 'other', 'tragedy'):16, ('m', 'other', 'history'):17}

        with open('../characteristics.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if re.match(target+"_", row[0]) or target == row[0]:
                    fit_set.append(class_list[row[trait_indeces[trait]]])
                    # fit_set.append(class_list[(row[1], row[2], row[3])])
        return fit_set

    def get_fit_char(self, char, trait):
        '''
        @param char: the string character withheld
        @param trait: "gender", "role", or "genre." The class on which the classifier
            is deciding, specified in arguments to main
        @return fit_set: a list containing correct classification of every character
            other than the withheld
        '''
        fit_set = []
        trait_indeces = {'gender':1, 'role':2, 'genre':3}
        class_list = {'f':0, 'm':1, 'protag':2, 'antag':3, 'fool':4, 'other':5, 'comedy':6, 'tragedy':7, 'history':8}

        with open('../characteristics.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if char != row[0] and row[0] != 'character':
                    fit_set.append(class_list[row[trait_indeces[trait]]])
                    # fit_set.append(class_list[(row[1], row[2], row[3])])
        return fit_set

    def get_new_data(target, data_file):
        '''
        @param target: a string of the play or char to be predicted by the naive Bayes
        @param data_file: a string of either the feature or phoneme percent file,
            specified in the arguments to main
        @return new_data: an array of the percent distribution(s) for the selected
            character(s)
        '''
        new_data = []
        with open(data_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if re.match(target+"_", row[0]) or target == row[0]:
                    new_data.append(list(map(lambda x: float(x), (row[1:]))))
        return numpy.array(new_data)

    def predict_data_play(self, play, trait, data_file):
        '''
        @param play: the play whose class we wish to predict
        @param trait: the trait we are attempting to classify
        @param data_file: the file containing either phoneme or feature data
        @return predicted: a vector of the classifications predicted by the naive Bayes
            for the characters in the play
        @return actual: a vector of the actual classifications for those characters
        '''

        training_choices = GLOBAL_PLAY_LIST.copy()
        training_choices.remove(play)

        # random_training = random.randint(0,37)
        # training_play = training_choices[random_training]

        training_data = []
        fit = []

        for training_play in training_choices:
            play_fit = self.get_fit(training_play, trait)
            fit.append(play_fit)
            play_data = self.get_training_data_play(training_play, data_file)
            training_data.append(play_data)


        training_data = numpy.array(sum(training_data, []))
        fit = numpy.array(sum(fit, []))


        # gnb = GaussianNB()
        # gnb.fit(training_data, fit)
        mnb  = MultinomialNB()
        mnb.fit(training_data, fit)

        predict_data = self.get_new_data(play, data_file)
        predicted = mnb.predict(predict_data)
        # predicted = gnb.predict(predict_data)
        actual = numpy.array(get_fit(play, trait))

        return predicted, actual

    def predict_data_char(self, char, trait, data_file, weighted):
        '''
        @param char: the char whose class we wish to predict
        @param trait: the trait we are attempting to classify
        @param data_file: the file containing either phoneme or feature data
        @return predicted: an int of the classification predicted by the naive Bayes
            for the character
        @return actual: an int of the actual classifications for that characters
        '''
        # random_training = random.randint(0,37)
        # training_play = training_choices[random_training]

        predict_data, training_data = self.get_training_data_char(char, data_file)
        fit = numpy.array(self.get_fit_char(char, trait))

        gnb = GaussianNB()
        if weighted == "True":
            sample_weight = self.get_sample_weight(char)
            gnb.fit(training_data, fit, sample_weight=sample_weight)
        else:
            gnb.fit(training_data, fit)

        # mnb  = MultinomialNB()
        # mnb.fit(training_data, fit)

        # predict_data = get_new_data(char, data_file)
        predict_data.reshape(1, -1)
        # predicted = mnb.predict(predict_data)
        predicted = gnb.predict(predict_data)
        actual = numpy.array(self.get_fit(char, trait))

        return predicted, actual

    def print_confusion_matrix(self, confusion_dictionary, trait, weighted):
        '''
        @param confusion_dictionary: a dictionary containing the tallies of actual and
        predicted values for a data set. Format: {actual1:{predicted1:#, predicted2:#,...},actual2:{predicted1:#, ...},...}
        @param trait: the trait for which the confusion dictionary was calculated
        @return nothing
        Prints the given confusion dictionary to a csv file
        '''
        class_list = {0:'f', 1:'m', 2:'protag', 3:'antag', 4:'fool', 5:'other', 6:'comedy', 7:'tragedy', 8:'history'}
        with open("confusion_matrices/{0}_{1}_weighted.csv".format(trait, weighted), 'w') as result:
            result.write('predicted')
            for i in range(9):
                if i in confusion_dictionary:
                    result.write(','+class_list[i])
            result.write('\n')
            for j in range(9):
                if j in list(list(confusion_dictionary.values())[0].keys()):
                    result.write(class_list[j])
                    for i in range(9):
                        if i in confusion_dictionary and j in confusion_dictionary[i]:
                            result.write(','+str(confusion_dictionary[i][j]))
                    result.write('\n')

    def generate_predictions(self):
        '''
        Currently either withholds and classifies one character or one play at a time
        based on whether or not the first arg contains an underscore. Classification
        is done for the specified characteristic, by the linguistic characterization
        given in the 3rd arg

        The character version currently prints the proportion of false positives, false
        negatives, and swaps, assuming that role was chosen as the trait.

        The play version prints the average Hamming distance between the predicted and
        actual vectors
        '''
        if len(sys.argv) < 4:
            #this is kind of a lie with the current state of my main but w/e w/e
            print("Usage: naive_bayes.py <weighted> <characteristic> <[p]honeme, [f]eature, or [c]ombined>")
            sys.exit()
        else:
            weight = sys.argv[1]
            trait = sys.argv[2]
            data = sys.argv[3]

        data_file = None

        if data[0].lower() == 'p':
            data_file = "../../tagging/phonemefreq/masterData.csv"
        elif data[0].lower() == 'f':
            data_file = "../../tagging/features/percentData.csv"
        elif data[0].lower() == 'c':
            data_file = '../../tagging/combinedData.csv'
        else:
            while data_file is None:
                data = input("Invalid data type. Please enter \"[p]honeme\", \"[f]eature\", or \"[c]ombined\" ")
                if data[0].lower() == 'p':
                    data_file = "../../tagging/phonemefreq/masterData.csv"
                elif data[0].lower() == 'f':
                    data_file = "../../tagging/features/percentData.csv"
                elif data[0].lower() == 'c':
                    data_file = '../../tagging/combinedData.csv'

        # if "_" in play_code:
        ret_dict = {}
        predicted_list = []
        actual_list = []
        with open('../characteristics.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != "character":
                    char = row[0]
                    predicted, actual = self.predict_data_char(char, trait, data_file, weight)
                    actual_list.extend(actual)
                    predicted_list.extend(predicted)
                    if actual[0] not in ret_dict:
                        ret_dict[actual[0]] = {}
                        ret_dict[actual[0]][predicted[0]] = 1
                    elif predicted[0] not in ret_dict[actual[0]]:
                        ret_dict[actual[0]][predicted[0]] = 1
                    else:
                        ret_dict[actual[0]][predicted[0]] += 1
        for value in ret_dict:
            for possible in ret_dict:
                if possible not in ret_dict[value]:
                    ret_dict[value][possible] = 0
        self.print_confusion_matrix(ret_dict, trait, weight)
        return predicted_list, actual_list

        '''
        Holdover from by-play training option
        '''
        # else:
        #     hamm_dist = []
        #     for play in GLOBAL_PLAY_LIST:
        #         predicted, actual = predict_data_play(play, trait, data_file)
        #         hamm_dist.append(hamming(predicted, actual))
        #     print(statistics.mean(hamm_dist))
        # print("Predicted:", gnb.predict(predict_data))
        # print("Actual:", numpy.array(get_fit(play_code, trait))

def main():
    nb = Naive_Bayes()
    nb.generate_predictions()
    
if __name__ == "__main__":
    main()
