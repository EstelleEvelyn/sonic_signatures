import csv
from operator import itemgetter

class Distinct:
    def __init__(self):
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

        self.antag_feature_count = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
            'stop':0, 'glottal':0, 'linguaalveolar':0, 'linguapalatal':0, 'labiodental':0,
            'bilabial':0, 'linguavelar':0,'linguadental':0, 'voiced':0, 'voiceless':0,
            'sibilant':0, 'nonsibilant':0, 'sonorant':0, 'nonsonorant':0, 'coronal':0,
            'noncoronal':0, 'monophthong':0, 'diphthong':0, 'central':0, 'front':0, 'back':0,
            'tense':0, 'lax':0, 'rounded':0,'unrounded':0}
        self.protag_feature_count = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
            'stop':0, 'glottal':0, 'linguaalveolar':0, 'linguapalatal':0, 'labiodental':0,
            'bilabial':0, 'linguavelar':0,'linguadental':0, 'voiced':0, 'voiceless':0,
            'sibilant':0, 'nonsibilant':0, 'sonorant':0, 'nonsonorant':0, 'coronal':0,
            'noncoronal':0, 'monophthong':0, 'diphthong':0, 'central':0, 'front':0, 'back':0,
            'tense':0, 'lax':0, 'rounded':0,'unrounded':0}

        self.antag_phoneme_count = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
            'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
            'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
            'DH':0,'D':0,'CH':0}
        self.protag_phoneme_count = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
            'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
            'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
            'DH':0,'D':0,'CH':0}

        self.protag_sum = 0
        self.antag_sum = 0

    def phoneme_totals(self):
        with open("../tagging/phonemefreq/masterCounts.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('filename') in self.protag_list:
                    for item in row:
                        if item in self.protag_phoneme_count:
                            self.protag_phoneme_count[item] += int(row.get(item))
                            self.protag_sum += int(row.get(item))
                if row.get('filename') in self.antag_list:
                    for item in row:
                        if item in self.antag_phoneme_count:
                            self.antag_phoneme_count[item] += int(row.get(item))
                            self.antag_sum += int(row.get(item))


    def feature_totals(self):
        with open("../tagging/features/countData.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('filename') in self.protag_list:
                    for item in row:
                        if item in self.protag_feature_count:
                            self.protag_feature_count[item] += int(row.get(item))
                if row.get('filename') in self.antag_list:
                    for item in row:
                        if item in self.antag_feature_count:
                            self.antag_feature_count[item] += int(row.get(item))

    def percent_features(self):
        self.feature_totals()
        percent_list = []
        for item in self.protag_feature_count:
            antag_count = self.antag_feature_count[item]
            protag_count = self.protag_feature_count[item]
            total = float(antag_count + protag_count)
            percent_list.append([item, protag_count/total])
        percent_list.sort(key=itemgetter(1), reverse=True)
        return percent_list

    def percent_phonemes(self):
        self.phoneme_totals()
        percent_list = []
        for item in self.protag_phoneme_count:
            antag_count = self.antag_phoneme_count[item]
            protag_count = self.protag_phoneme_count[item]
            total = float(antag_count + protag_count)
            percent_list.append([item, protag_count/total])
        percent_list.sort(key=itemgetter(1), reverse=True)
        return percent_list

    def normalize(self):
        norm_dist = {}
        for phoneme in self.protag_phoneme_count:


def main():
    dist = Distinct()
    features = dist.percent_features()
    phonemes = dist.percent_phonemes()

    print("features: ", features)
    print("phonemes: ", phonemes)

if __name__ == "__main__":
    main()
