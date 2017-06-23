import scikit
import numpy
from sklearn.naive_bayes import GaussianNB
import csv

'''
naive_bayes.py
Estelle Bayer, Summer 2017
A program to classify Shakespearean characters based on the phonetic features of
their speech
'''
def get_training_fit(dataset):
    #cross-reference some known quantity of traits
    fit_set = []
    return fit_set

def get_new_data():
    #get some new data
    new_data = []
    return new_data

def main():
    training_data = []
    with open("../tagging/features/percentData.csv", 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            training_data.append(row)
    gnb = GaussianNB()
    fit = get_training_fit(training_data)

    predict_data = get_new_data()
    print(gnb.predict(predict_data))
