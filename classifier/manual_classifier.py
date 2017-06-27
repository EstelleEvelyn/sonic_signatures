import csv
import re
from operator import itemgetter
'''
manual_classifier.py
Estelle Bayer, Summer 2017
A program used to assign traits to Shakespearean characters, for use in training
and testing a classifier based on sonic signature data
'''
class manual_classifier:
    def __init__(self):
        self.female_list = ['AWW_Helen', 'AWW_Countess', 'AWW_Diana', 'AWW_Widow', 'AWW_Mariana',
                        'Ant_Cleopatra', 'Ant_Charmian', 'Ant_Octavia', 'Ant_Iras', 'AYL_Rosalind',
                        'AYL_Celia',  'AYL_Phoebe', 'AYL_Audrey', 'Err_Adriana', 'Err_Abbess',
                        'Err_Luciana', 'Err_Courtesan','Err_Luce', 'Cor_Volumnia', 'Cor_Valeria',
                        'Cor_Virgilia', 'Cor_Gentlewoman', 'Cym_Imogen', 'Cym_Queen', 'Cym_LADIES.QUEEN',
                        'Cym_LADIES.IMOGEN', 'Cym_LADIES.QUEEN.0.1', 'Ham_Ophelia', 'Ham_Gertrude',
                        'Ham_PLAYERS.Queen', '1H4_LadyPercy', '1H4_MistressQuickly', '2H4_MistressQuickly',
                        '2H4_DollTearsheet', '2H4_LadyPercy', '2H4_LadyNorthumberland', 'H5_Katherine',
                        'H5_Alice', 'H5_MistressQuickly', 'H5_QueenOfFrance', '1H6_Pucelle',
                        '1H6_Countess', '1H6_QueenMargaret', '2H6_QueenMargaret', '2H6_DuchessOfGloucester',
                        '2H6_SimpcoxWife', '2H6_Jourdain', '3H6_QueenMargaret', '3H6_QueenElizabeth',
                        '3H6_LadyBona', 'H8_Katherine', 'H8_OldLady', 'H8_Anne', 'H8_LADIES.KATERINE.0.1',
                        'H8_LADIES.KATHERINE.Patience', 'JC_Portia', 'JC_Calphurnia', 'Jn_Constance',
                        'Jn_QueenEleanor', 'Jn_Blanche', 'Jn_LadyFaulconbridge', 'Lr_Goneril',
                        'Lr_Cordelia', 'Lr_Regan', 'LLL_Princess', 'LLL_Rosaline', 'LLL_Katherine',
                        'LLL_Maria', 'LLL_Jaquenetta', 'Mac_LadyMacbeth', 'Mac_LadyMacduff',
                        'Mac_WITCHES.1', 'Mac_WITCHES.2', 'Mac_WITCHES.3','Mac_Hecate', 'MM_Isabella',
                        'MM_Mariana', 'MM_Juliet', 'MM_Nun', 'MV_Portia', 'MV_Nerissa', 'MV_Jessica',
                        'Wiv_AnnePage', 'Wiv_MistressQuickly', 'Wiv_MistressFord', 'Wiv_MistressPage',
                        'MND_Helena', 'MND_Hermia', 'MND_Titania', 'MND_Hippolyta', 'Ado_Beatrice',
                        'Ado_Hero', 'Ado_Margaret', 'Ado_Ursula', 'Oth_Desdemona', 'Oth_Bianca',
                        'Oth_Emilia', 'Per_Marina', 'Per_Bawd', 'Per_Dionyza', 'Per_Thaisa',
                        'Per_Lychordia', 'Per_Diana', 'Per_Daughter', 'R2_Queen', 'R2_DuchessofYork',
                        'R2_DuchessOfGloucester', 'R2_LADIES.0.1', 'R3_QueenElizabeth',
                        'R3_QueenMargaret', 'R3_LadyAnne', 'R3_DuchessofYork', 'R3_ClarencesDaughter',
                        'Rom_Juliet', 'Rom_Nurse', 'Rom_LadyCapulet', 'Rom_LadyMontague', 'Shr_Bianca',
                        'Shr_Katherine', 'Shr_Widow', 'Shr_Hostess', 'Tmp_Miranda', 'Tmp_SPIRITS.Ceres',
                        'Tmp_SPIRITS.Iris', 'Tmp_SPIRITS.Juno', 'Tim_Timandra', 'Tim_LADIES',
                        'Tim_LADIES.0.1', 'Tim_Phrynia', 'Tit_Tamora', 'Tit_Lavinia', 'Tit_Nurse',
                        'Tro_Cressida', 'Tro_Cassandra', 'Tro_Helen', 'Tro_Andromache', 'Tro_Helenus',
                        'TN_Viola', 'TN_Olivia', 'TN_Maria', 'TGV_Julia', 'TGV_Silvia', 'TGV_Lucetta',
                        'TNK_Emilia', 'TNK_Daughter', 'TNK_Hippolyta', 'TNK_QUEENS.1', 'TNK_QUEENS.2',
                        'TNK_QUEENS.3', 'TNK_Woman', 'TNK_COUNTRYWOMEN.0.1', 'WT_Paulina',
                        'WT_Hermione', 'WT_Perdita', 'WT_Mopsa', 'WT_Emilia', 'WT_Dorcas',
                        'WT_LADIES.0.1', 'WT_LADIES.0.2']

        self.protag_list = ['AWW_Helen', 'Ant_Antony', 'AYL_Rosalind', 'Err_AntipholusOfSyracuse',
                        'Cor_Coriolanus', 'Cym_Imogen', 'Ham_Hamlet', '1H4_HenryV', '2H4_HenryV',
                        'H5_HenryV', '1H6_HenryVI', 'H8_HenryVIII', 'JC_Brutus', 'Jn_KingJohn',
                        'Lr_Lear', 'LLL_King', 'Mac_Macbeth', 'MM_Duke', 'MV_Portia',
                        'Wiv_Mistrss_Page', 'MND', 'Ado_Beatrice', 'Oth_Othello', 'Per_Pericles',
                        'R2_RichardII', 'R3_RichardIII', 'Rom_Romeo', 'Shr_Petruchio', 'Tmp_Prospero',
                        'Tim_Timon', 'Tit_Titus', 'Tro_Troilus', 'TN_Viola', 'TGV_Valentine',
                        'TNK_Theseus', 'WT_Leontes']

        self.antag_list = ['AWW_Bertram', 'Ant_Caesar', 'AYL_DukeFredrick', 'Err_AntipholusOfEphesus',
                        'Cor_TRIBUNES.Brutus', 'Cym_Iachimo', 'Ham_Claudius', '1H4_Hotspur',
                        '2H4_ChiefJustice', 'H5_Dauphin', '1H6_Charles', 'H8_Wolsey',
                        'JC_Antony', 'Jn_KingPhilip', 'Lr_Goneril', 'LLL_Princess', 'MM_Angelo',
                        'MV_Shylock', 'Wiv_Falstaff', 'MND', 'Ado_DonJohn', 'Oth_Iago', 'Per_Antiochus',
                        'R2_HenryIV', 'R3_RichardIII', 'Rom_Tybalt', 'Tmp_Antonio', 'Tit_Aaron',
                        'TN_Malvolio', 'TGV_Proteus', 'WT_Polixenes']

        self.comedy_list = ['AWW', 'AYL', 'Err', 'LLL', 'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Per',
                        'Shr', 'Tmp', 'TN', 'TNK', 'TGV', 'WT']

        self.tragedy_list = ['Ant', 'Cor', 'Cym', 'Ham', 'JC', 'Lr', 'Mac', 'Oth', 'Rom',
                        'Tim', 'Tit', 'Tro']

        self.history_list = ['1H4', '2H4', 'H5', '1H6', '2H6', '3H6', 'H8', 'Jn', 'R2', 'R3']

        self.characteristic_dict = {}
        with open("../tagging/features/percentData.csv", 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                self.characteristic_dict[row.get('filename')] = {}

    def sort_gender(self, char):
        '''
        Adds a dictionary entry for every character specifying their gender
        '''
        if char in self.female_list:
            self.characteristic_dict[char]['gender'] = 'f'
        else:
            self.characteristic_dict[char]['gender'] = 'm'

    def sort_role(self, char):
        '''
        Adds a dictionary entry for every character specifying their role {protag, antag, other}
        '''
        if char in self.protag_list:
            self.characteristic_dict[char]['role'] = 'protag'
        elif char in self.antag_list:
            self.characteristic_dict[char]['role'] = 'antag'
        else:
            self.characteristic_dict[char]['role'] = 'other'

    def sort_genre(self, char):
        '''
        Adds a dictionary entry for every character specifying the genre of their play
        {comedy, history, tragedy}
        '''

        for comedy in self.comedy_list:
            if re.match(comedy+"_", char):
                self.characteristic_dict[char]['genre'] = 'comedy'
                return

        for tragedy in self.tragedy_list:
            if re.match(tragedy+"_", char):
                self.characteristic_dict[char]['genre'] = 'tragedy'
                return

        for history in self.history_list:
            if re.match(history+"_", char):
                self.characteristic_dict[char]['genre'] = 'history'
                return

    def update_char_dict(self):
        '''
        Updates the gender, role, and genre of every character, and returns the characteristic_dict
        '''
        with open("../tagging/features/percentData.csv", 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                char = row.get('filename')
                self.sort_gender(char)
                self.sort_role(char)
                self.sort_genre(char)
        return self.characteristic_dict

def main():
    classifier = manual_classifier()
    char_dict = classifier.update_char_dict()
    data_list = []
    with open('characteristics.csv', 'w') as result:
        result.write('character,gender,role,genre\n')
        for item in char_dict:
            data_list.append([item, char_dict[item]['gender'],
            char_dict[item]['role'], char_dict[item]['role']])
        data_list.sort(key = itemgetter(0))
        csv.writer(result).writerows(data_list)


if __name__ == '__main__':
    main()
