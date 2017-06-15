class Tagger:
    def __init__(self):
        self.dictionary_classifier = {'AA':[],
            'AE':[],
            'AH':[],
            'AO':[],
            'AW':[],
            'AY':[],
            'B':['stop', 'bilabial', 'voiced'],
            'CH':['affricate', 'linguaalveolar', 'voiceless'],
            'D':['stop', 'linguaalveolar', 'voiced'],
            'DH':['fricative', 'linguadental', 'voiced'],
            'EH':[],
            'ER':[],
            'EY':[],
            'F':['fricative', 'labiodental', 'voiceless'],
            'G':['stop', 'linguavelar', 'voiced'],
            'HH':['fricative', 'glottal', 'voiceless'],
            'IH':[],
            'IY':[],
            'JH':['affricate', 'linguaalveolar', 'voiced'],
            'K':['stop', 'linguavelar', 'voiceless'],
            'L':['liquid', 'linguaalveolar', 'voiced'],
            'M':['nasal', 'bilabial', 'voiced'],
            'N':['nasal', 'linguaalveolar', 'voiced'],
            'NG':['nasal', 'linguavelar', 'voiced'],
            'OW':['diphthong'],
            'OY':['diphthong'],
            'P':['stop', 'bilabial', 'voiceless'],
            'R':['liquid', 'linguapalatal', 'voiced'],
            'S':['fricative', 'linguaalveolar', 'voiceless'],
            'SH':['fricative', 'linguapalatal', 'voiceless'],
            'T':['stop', 'linguaalveolar', 'voiceless'],
            'TH':['fricative', 'linguadental', 'voiceless'],
            'UH':['monophthong'],
            'UW':['monophthong'],
            'V':['fricative', 'labiodental', 'voiced'],
            'W':['glide', 'bilabial', 'voiced'],
            'Y':['glide', 'linguapalatal', 'voiced'],
            'Z':['fricative', 'linguaalveolar', 'voiced'],
            'ZH':['fricative', 'linguapalatal', 'voiced']}

    def counts(self, read_file):
        return_dict = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
                        'stop':0, 'monophthong':0, 'diphthong':0, 'glottal':0,
                        'linguaalveolar':0, 'linguapalatal':0, 'labiodental':0, 'bilabial':0,
                        'linguavelar':0,'linguadental':0, 'voiced':0, 'voiceless':0}
        text = read_file.read().split()
        for phoneme in text:
            if phoneme[-1] in "0123456789":
                phoneme = phoneme[:-1]
            if phoneme != ',':
                characteristics = DICTIONARY_CLASSIFIER[phoneme]
                for characteristic in characteristics:
                    return_dict[characteristic] += 1

        return return_dict



def main():
    counter = Tagger()
    with open("dest/Cym_Cymbeline.txt", 'r') as read_file:
        print(counter.counts(read_file))

if __name__ == "__main__":
    main()
