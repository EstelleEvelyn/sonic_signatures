import numpy
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from scipy.spatial.distance import hamming
import csv
import re
import sys
import statistics
import random
import naive_bayes
import random

def main():
        prot_ant_list = ['AWW_Helen', 'Ant_Antony', 'AYL_Rosalind', 'Err_AntipholusOfSyracuse',
                    'Cor_Coriolanus', 'Cym_Imogen', 'Ham_Hamlet', '1H4_HenryV', '2H4_HenryV',
                    'H5_HenryV', '1H6_HenryVI', 'H8_HenryVIII', 'JC_Brutus', 'Jn_KingJohn',
                    'Lr_Lear', 'LLL_King', 'Mac_Macbeth', 'MM_Duke', 'MV_Portia',
                    'Wiv_MistressPage', 'Ado_Beatrice', 'Oth_Othello', 'Per_Pericles',
                    'R2_RichardII', 'R3_RichardIII', 'Rom_Romeo', 'Shr_Petruchio', 'Tmp_Prospero',
                    'Tim_Timon', 'Tit_Titus', 'Tro_Troilus', 'TN_Viola', 'TGV_Valentine',
                    'TNK_Theseus', 'WT_Leontes', 'AWW_Bertram', 'Ant_Octavius', 'AYL_DukeFrederick',
                    'Err_AntipholusOfEphesus', 'Cor_TRIBUNES.Brutus', 'Cym_Iachimo',
                    'Ham_Claudius', '1H4_Hotspur', '2H4_ChiefJustice', 'H5_Dauphin',
                    '1H6_Charles', 'H8_Wolsey', 'JC_Antony', 'Jn_KingPhilip', 'Lr_Goneril',
                    'LLL_Princess', 'MM_Angelo', 'MV_Shylock', 'Wiv_Falstaff',
                    'Ado_DonJohn', 'Oth_Iago', 'Per_Antiochus', 'R2_HenryIV', 'R3_RichardIII',
                     'Rom_Tybalt', 'Tmp_Antonio', 'Tit_Aaron', 'TN_Malvolio', 'TGV_Proteus', 'WT_Polixenes']


        class_list = {'f':0, 'm':1, 'protag':2, 'antag':3, 'other':4, 'comedy':5, 'tragedy':6, 'history':7}

        random.shuffle(prot_ant_list)

        false_pos = 0
        false_neg = 0
        total = 0
        for char in prot_ant_list:
            training_data = []
            fit_set = []
            with open('../tagging/phonemefreq/masterData.csv', 'r') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    if char != row[0] and row[0] in prot_ant_list:
                        training_data.append(list(map(lambda x: float(x), row[1:])))
            training_data = numpy.array(training_data)

            with open('characteristics.csv', 'r') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    if char != row[0] and row[0] in prot_ant_list:
                        fit_set.append(class_list[row[2]])
            fit_set = numpy.array(fit_set)

            # mnb  = MultinomialNB()
            # mnb.fit(training_data, fit_set)

            gnb = GaussianNB()
            gnb.fit(training_data, fit_set)

            predict_data = naive_bayes.get_new_data(char, '../tagging/phonemefreq/masterData.csv')
            predict_data.reshape(1, -1)
            # predicted = mnb.predict(predict_data)
            predicted = gnb.predict(predict_data)

            actual = numpy.array(naive_bayes.get_fit(char, 'role'))

            if predicted > actual:
                false_ant += 1
            elif predicted < actual:
                false_prot += 1
            total += 1


            print(char, "predicted:",predicted, "actual:",actual )
        print(false_ant/float(total), false_prot/float(total))


main()
