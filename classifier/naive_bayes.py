import scikit
import numpy
from sklearn.naive_bayes import GaussianNB
import csv
import re

'''
naive_bayes.py
Estelle Bayer, Summer 2017
A program to classify Shakespearean characters based on the phonetic features of
their speech
'''
def get_training_fit(dataset):
    #cross-reference some known quantity of traits
    fit_set = {'AWW_ATTENDANTS.KING.0.1':'M', 'AWW_ATTENDANTS.KING.0.2':'M', 'AWW_Bertram':'M',
            'AWW_Countess':'F', 'AWW_Diana':'F', 'AWW_Duke':'M', 'AWW_Epilogue':'M',
            'AWW_Fool':'M', 'AWW_GENTLEMEN.1':'M', 'AWW_GENTLEMEN.3':'M', 'AWW_GENTLEMEN.3':'M',
            'AWW_Helen':'F', 'AWW_King':'M', 'AWW_Lafew':'M', 'AWW_LORDS.COURT.1':'M',
            'AWW_LORDS.COURT.2':'M', 'AWW_LORDS.COURT.3':'M', 'AWW_LORDS.COURT.4':'M',
            'AWW_LORDS.DUMAINE.1':'M', 'AWW_Mariana':'F', 'AWW_Page':'M', 'AWW_Parolles':'M',
            'AWW_Servant':'M', 'AWW_SOLDIERS.0.1':'M', 'AWW_SOLDIERS.Interpreter':'M',
            'AWW_SOLDIERS':'M', 'AWW_Steward':'M', 'AWW_Widow':'F'}
    return fit_set

def get_new_data():
    #get some new data
    new_data = []
    with open("../tagging/features/percentData.csv", 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if re.match('AYL_', row.get('filename')):
                training_data.append(row)
    return new_data

def main():
    training_data = []
    with open("../tagging/features/percentData.csv", 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if re.match('AWW_', row.get('filename')):
                training_data.append(row)
    gnb = GaussianNB()
    fit = get_training_fit(training_data)

    predict_data = get_new_data()
    print(gnb.predict(predict_data))
