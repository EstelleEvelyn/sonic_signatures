import numpy
from sklearn.naive_bayes import GaussianNB
from double_bayes import DoubleBayes
import csv
import math
import sys

def get_sample_weight(char):
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


def get_training_data_char(char):
    '''
    @param char: the string char being withheld
    @return training: a list of nasal feature percent for every character other than
        the withheld char
    @return withheld: the nasal feature percent for the withheld character
    '''
    training = []
    withheld = []
    with open('../../tagging/features/percentData.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if char != row[0] and row[0] != 'filename':
                training.append(list(map(lambda x: float(x), row[1:])))
            elif char == row[0] and row[0] != 'filename':
                withheld.append(list(map(lambda x: float(x), row[1:])))
    return withheld, training

def get_fit_char(char):
    '''
    @param char: the string character withheld
    @return fit_set: a list containing correct classification of every character
        other than the withheld
    '''
    fit_set = []
    class_list = {'protag':0, 'antag':1, 'fool':2, 'other':3}

    with open('../characteristics.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if char != row[0] and row[0] != 'character':
                fit_set.append(class_list[row[2]])
    return fit_set

def get_actual(char):
    '''
    @param char: a string character for which we want to obtain
        the role information
    @return actual_set: a list containing the correct classification for the
        target character
    '''
    actual_set = []
    class_list = {'protag':0, 'antag':1, 'fool':2, 'other':3}

    with open('../characteristics.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if char == row[0]:
                actual_set.append(class_list[row[2]])
                break
    return actual_set


def predict_data_char(char):
    '''
    @param char: the char whose class we wish to predict
    @return predicted: an int of the classification predicted by the naive Bayes
        for the character
    @return actual: an int of the actual classifications for that characters
    '''

    predict_data, training_data = get_training_data_char(char)
    training_data = numpy.array(training_data)
    fit = numpy.array(get_fit_char(char))

    sample_weight = get_sample_weight(char)

    gnb = GaussianNB()
    gnb.fit(training_data, fit, sample_weight = sample_weight)

    predict_data = numpy.array(predict_data)
    predict_data.reshape(1, -1)
    predicted = gnb.predict(predict_data)
    actual = numpy.array(get_actual(char))

    return predicted, actual

def print_confusion_matrix(confusion_dictionary):
    '''
    @param confusion_dictionary: a dictionary containing the tallies of actual and
    predicted values for a data set. Format: {actual1:{predicted1:#, predicted2:#,...},actual2:{predicted1:#, ...},...}
    @return nothing
    Prints the given confusion dictionary to a csv file
    '''
    class_list = {0:'protag', 1:'antag', 2:'fool', 3:'other'}
    with open("confusion_matrix_weighted.csv", 'w') as result:
        result.write('predicted')
        for i in range(4):
            result.write(','+class_list[i])
        result.write('\n')
        for j in range(4):
            result.write(class_list[j])
            for i in range(4):
                result.write(','+str(confusion_dictionary[i][j]))
            result.write('\n')

def main():
    if len(sys.argv) < 2:
        #this is kind of a lie with the current state of my main but w/e w/e
        print("Usage: naive_bayes.py <[s]ingle or [d]ouble>")
        sys.exit()
    else:
        iteration = sys.argv[1]

    if iteration[0].lower == 's':
        ret_dict = {}
        with open('../characteristics.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != "character":
                    char = row[0]
                    predicted, actual = predict_data_char(char)
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
        print_confusion_matrix(ret_dict)
    else:
        db  = DoubleBayes()
        db.generate_predictions(weighted = True)

if __name__ == "__main__":
    main()
