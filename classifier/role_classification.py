import csv
from operator import itemgetter
import statistics
import math

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

        self.consonants = ['B','CH','D','DH','F','G','HH','JH','K','L','M','N','NG',
            'P','R','S','SH','T','TH','V','W','Y','Z','ZH', 'fricative', 'affricate', 'glide', 'nasal',
            'liquid', 'stop', 'glottal', 'linguaalveolar', 'linguapalatal', 'labiodental', 'bilabial',
            'linguavelar', 'linguadental', 'voiced', 'voiceless', 'sibilant', 'nonsibilant',
            'sonorant', 'nonsonorant', 'coronal', 'noncoronal']
        self.vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW',
            'monophthong', 'diphthong', 'central', 'front', 'back', 'tense', 'lax', 'rounded','unrounded']

        self.antag_phoneme_count = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
            'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
            'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
            'DH':0,'D':0,'CH':0}
        self.protag_phoneme_count = {'B':0,'AA':0,'AE':0,'AH':0,'AO':0,'AW':0,'AY':0,'EH':0,'ER':0,'EY':0,
            'IH':0,'IY':0,'OW':0,'OY':0,'UH':0,'UW':0,'ZH':0,'Z':0,'Y':0,'W':0,'V':0,'TH':0,'T':0,
            'SH':0,'S':0,'R':0,'P':0,'NG':0,'N':0,'M':0,'L':0,'K':0,'JH':0,'HH':0,'G':0,'F':0,
            'DH':0,'D':0,'CH':0}

        self.protag_cons_sum = 0
        self.protag_vowel_sum = 0
        self.antag_cons_sum = 0
        self.antag_vowel_sum = 0

    def phoneme_totals(self):
        with open("../tagging/phonemefreq/masterCounts.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('filename') in self.protag_list:
                    for item in row:
                        if item in self.protag_phoneme_count:
                            self.protag_phoneme_count[item] += int(row.get(item))
                            if item in self.consonants:
                                self.protag_cons_sum += int(row.get(item))
                            else:
                                self.protag_vowel_sum += int(row.get(item))
                if row.get('filename') in self.antag_list:
                    for item in row:
                        if item in self.antag_phoneme_count:
                            self.antag_phoneme_count[item] += int(row.get(item))
                            if item in self.consonants:
                                self.antag_cons_sum += int(row.get(item))
                            else:
                                self.antag_vowel_sum += int(row.get(item))


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

    def z_features(self):
        p_pcts, a_pcts = self.percent_features()
        z_list = []
        for feature in self.protag_feature_count:
            with open("../statistics/feature_statistics.csv", 'r') as featfile:
                reader = csv.DictReader(featfile)
                for row in reader:
                    if row['feature'] == feature:
                        std_err = float(row['stdev']) # / math.sqrt(686)

                        protag_feat_mean = p_pcts[feature]
                        protag_z = (protag_feat_mean - float(row['mean'])) / std_err

                        antag_feat_mean = a_pcts[feature]
                        antag_z = (antag_feat_mean - float(row['mean'])) / std_err
                        break
                z_list.append((feature, (protag_z, antag_z)))
                z_list.sort(key = itemgetter(1), reverse=True)

        return z_list

    def z_phonemes(self):
        p_pcts, a_pcts = self.percent_phonemes()
        z_list = []
        for phoneme in p_pcts:
            with open("../statistics/phoneme_statistics.csv", 'r') as phonefile:
                reader = csv.DictReader(phonefile)
                for row in reader:
                    if row['phoneme'] == phoneme:
                        std_err = float(row['stdev'])# / math.sqrt(686)

                        protag_phon_mean = p_pcts[phoneme]
                        print(phoneme,protag_phon_mean, row['mean'], std_err)
                        protag_z = (protag_phon_mean - float(row['mean'])) / std_err

                        antag_phon_mean = a_pcts[phoneme]
                        antag_z = (antag_phon_mean - float(row['mean'])) / std_err
                        break
                z_list.append((phoneme, (protag_z, antag_z)))
                z_list.sort(key = itemgetter(1), reverse=True)

        return z_list

    def percent_phonemes(self):
        self.phoneme_totals()
        p_percent_dict = {}
        a_percent_dict = {}
        for item in self.protag_phoneme_count:
            antag_count = self.antag_phoneme_count[item]
            protag_count = self.protag_phoneme_count[item]
            p_total = self.protag_cons_sum + self.protag_vowel_sum
            a_total = self.antag_cons_sum + self.antag_vowel_sum
            p_percent_dict[item]=float(protag_count)/p_total
            a_percent_dict[item]=float(antag_count)/a_total
        return p_percent_dict, a_percent_dict

    def percent_features(self):
        self.feature_totals()
        p_percent_dict = {}
        a_percent_dict = {}
        for item in self.protag_feature_count:
            antag_count = self.antag_feature_count[item]
            protag_count = self.protag_feature_count[item]
            if item in self.consonants:
                p_percent_dict[item]=float(protag_count)/self.protag_cons_sum
                a_percent_dict[item]=float(antag_count)/self.antag_cons_sum
            else:
                p_percent_dict[item]=float(protag_count)/self.protag_vowel_sum
                a_percent_dict[item]=float(antag_count)/self.antag_vowel_sum
        return p_percent_dict, a_percent_dict

def main():
    dist = Distinct()
    phonemes = dist.z_phonemes()
    features = dist.z_features()

    print("features: ", features)
    print("phonemes: ", phonemes)

if __name__ == "__main__":
    main()
