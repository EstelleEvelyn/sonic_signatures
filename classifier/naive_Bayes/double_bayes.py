import numpy
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from scipy.spatial.distance import hamming
import csv
import re
import os
import sys

'''
double_bayes.py
Estelle Bayer, Summer 2017
A program designed to classify roles in Shakespearean plays by two naive Bayes
iterations: the first to determine whether a character is a special role, and the
second performed only on that subset to classify which role those characters fill
'''
class DoubleBayes:

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

    def get_training_data_initial(self,char, data_file):
        '''
        @param char: the string char being withheld
        @param data_file: a tring of either the phoneme percent or feature percent file,
            determined by arguments to main
        @return training: a list of percent distributions for every character other than
            the withheld char
        '''
        withheld = []
        training = []
        with open(data_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if char != row[0] and row[0] != 'filename':
                    training.append(list(map(lambda x: float(x), row[1:])))
                elif row[0] != 'filename':
                    withheld.append(list(map(lambda x: float(x), row[1:])))
        return numpy.array(withheld), numpy.array(training)

    def get_training_data_reserved(self, remaining_chars, data_file):
        '''
        @param remaining_chars: the list of chars not classified as other
        @param data_file: a string of either the phoneme percent or feature percent file,
            determined by arguments to main
        @return training: a list of percent distributions for every character other than
            the withheld char
        '''
        training = []
        with open(data_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] in remaining_chars and row[0] != 'filename':
                    training.append(list(map(lambda x: float(x), row[1:])))
        return training

    def get_fit_initial(self, char):
        '''
        @param char: the string character withheld
        @return fit_set: a list containing correct classification of every character
            other than the withheld as either a reserved role or other
        @return remaining: the list of characters whose class is "1", for use when
            the predicted character is not "other"
        '''
        fit_set = []
        remaining = []
        class_list = {'protag':1, 'antag':1, 'fool':1, 'other':0}

        with open('../characteristics.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if char != row[0] and row[0] != 'character':
                    fit_set.append(class_list[row[2]])
                    if class_list[row[2]] == 1:
                        remaining.append(row[0])
        return numpy.array(fit_set), remaining

    def get_fit_reserved(self, remaining_chars):
        '''
        @param remaining_chars: the list of characters whose roles are not "other"
        @return fit_set: a list containing correct classification of every character
            in the specified list
        '''
        fit_set = []
        class_list = {'protag':1, 'antag':2, 'fool':3}

        with open('../characteristics.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if row[0] in remaining_chars and row[0] != 'character':
                    fit_set.append(class_list[row[2]])
        return fit_set

    def get_actual(self, char):
        '''
        @param char: a string character for which we want to obtain
            the role information
        @return fit_set: a list containing the correct classification for the
            target character
        '''
        actual_set = []
        class_list = {'protag':1, 'antag':2, 'fool':3, 'other':0}

        with open('../characteristics.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if re.match(char+"_", row[0]) or char == row[0]:
                    actual_set.append(class_list[row[2]])
                    break
        return actual_set

    def predict_data_char(self, char, data_file, weighted):
        '''
        @param char: the char whose class we wish to predict
        @param data_file: the file containing either phoneme or feature data
        @return predicted: an int of the classification predicted by the naive Bayes
            for the character
        @return actual: an int of the actual classifications for that characters
        '''

        prediction_data, training_data_initial = self.get_training_data_initial(char, data_file)
        fit_initial, remaining = self.get_fit_initial(char)

        gnb = GaussianNB()
        if weighted:
            sample_weight = self.get_sample_weight(char)
            gnb.fit(training_data_initial, fit_initial, sample_weight = sample_weight)
        else:
            gnb.fit(training_data_initial, fit_initial)

        prediction_data.reshape(1, -1)
        initial_predicted = gnb.predict(prediction_data)

        if initial_predicted == 1:

            if char in remaining:
                remaining.remove(char)

            training_data_reserved = numpy.array(self.get_training_data_reserved(remaining, data_file))
            fit_reserved = numpy.array(self.get_fit_reserved(remaining))

            gnb.fit(training_data_reserved, fit_reserved)
            remaining_predicted = gnb.predict(prediction_data)

            initial_predicted = remaining_predicted

        predicted = initial_predicted

        actual = numpy.array(self.get_actual(char))

        return predicted, actual

    def print_confusion_matrix(self, confusion_dictionary, weighted, data):
        '''
        @param confusion_dictionary: a dictionary containing the tallies of actual and
        predicted values for a data set. Format: {actual1:{predicted1:#, predicted2:#,...},actual2:{predicted1:#, ...},...}
        @return nothing
        Prints the given confusion dictionary to a csv file
        '''
        class_list = {1:'protag', 2:'antag', 3:'fool', 0:'other'}
        with open("confusion_matrices/double_{0}_{1}.csv".format(data, weighted), 'w') as result:
        # with open("confusion_matrix_double_combined.csv", 'w') as result:
            result.write('predicted')
            for i in range(4):
                result.write(','+class_list[i])
            result.write('\n')
            for j in range(4):
                result.write(class_list[j])
                for i in range(4):
                    result.write(','+str(confusion_dictionary[i][j]))
                result.write('\n')

    def generate_predictions(self, weighted = False):
        '''
        First classifies whether every given character is a special role or "other".
        In the special case, then classifies which role the character fills.
        Prints the results as a confusion matrix to a csv file
        '''
        if len(sys.argv) < 2:
            #this is kind of a lie with the current state of my main but w/e w/e
            print("Usage: naive_bayes.py <weighted> <[p]honeme, [f]eature, or [c]ombined>")
            sys.exit()
        elif len(sys.argv) == 2:
            data = sys.argv[1]
        else:
            data = sys.argv[2]
            weighted = sys.argv[1]

        data_file = None

        if data[0].lower() == 'p':
            data_file = "../../tagging/phonemefreq/masterData.csv"
        elif data[0].lower() == 'f':
            data_file = "../../tagging/features/percentData.csv"
        elif data[0].lower() == 'c':
            data_file = "../../tagging/combinedData.csv"
        else:
            while data_file is None:
                data = input("Invalid data type. Please enter \"[p]honeme\" or \"[f]eature\"")
                if data[0].lower() == 'p':
                    data_file = "../../tagging/phonemefreq/masterData.csv"
                elif data[0].lower() == 'f':
                    data_file = "../../tagging/features/percentData.csv"
                elif data[0].lower() == 'c':
                    data_file = "../../tagging/combinedData.csv"

        ret_dict = {}
        predicted_list = []
        actual_list = []
        with open('../characteristics.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != "character":
                    char = row[0]
                    predicted, actual = self.predict_data_char(char, data_file, weighted)
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
        self.print_confusion_matrix(ret_dict, data, weighted)
        return predicted_list, actual_list

def main():
    db = DoubleBayes()
    db.generate_predictions()

if __name__ == "__main__":
    main()
