from nltk_sonic_tagging import Transcriber

class Tagger:
    def __init__(self):
        self.dictionary_classifier = {'AA':['monophthong', 'back'],
            'AE':['monophthong', 'front'],
            'AH':['monophthong', 'central'],
            'AO':['monophthong', 'back'],
            'AW':['diphthong'],
            'AY':['diphthong'],
            'B':['stop', 'bilabial', 'voiced'],
            'CH':['affricate', 'linguaalveolar', 'voiceless'],
            'D':['stop', 'linguaalveolar', 'voiced'],
            'DH':['fricative', 'linguadental', 'voiced'],
            'EH':['monophthong', 'front'],
            'ER':['monophthong', 'central'],
            'EY':['diphthong'],
            'F':['fricative', 'labiodental', 'voiceless'],
            'G':['stop', 'linguavelar', 'voiced'],
            'HH':['fricative', 'glottal', 'voiceless'],
            'IH':['monophthong', 'front'],
            'IY':['monophthong', 'front'],
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
            'UH':['monophthong', 'back'],
            'UW':['monophthong', 'back'],
            'V':['fricative', 'labiodental', 'voiced'],
            'W':['glide', 'bilabial', 'voiced'],
            'Y':['glide', 'linguapalatal', 'voiced'],
            'Z':['fricative', 'linguaalveolar', 'voiced'],
            'ZH':['fricative', 'linguapalatal', 'voiced']}

    def counts(self, read_file):
        return_dict = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
                        'stop':0, 'monophthong':0, 'diphthong':0, 'glottal':0,
                        'linguaalveolar':0, 'linguapalatal':0, 'labiodental':0, 'bilabial':0,
                        'linguavelar':0,'linguadental':0, 'voiced':0, 'voiceless':0,
                        'central':0, 'front':0, 'back':0}
        text = read_file.read().split()
        for phoneme in text:
            if phoneme[-1] in "0123456789":
                phoneme = phoneme[:-1]
            if phoneme != ',':
                characteristics = self.dictionary_classifier[phoneme]
                for characteristic in characteristics:
                    return_dict[characteristic] += 1

        return return_dict

    def count_all_texts(self):
        transcriber = Transcriber()
        play_code_list = transcriber.get_play_code_list()
        for play in play_code_list:
            character_list = transcriber.get_character_list(play)
            for character in character_list:
                filename = play+"_"+character
                with open ("dest/{}.txt".format(filename), 'r') as source:
                    with open("counts/{}.txt".format(filename), 'w') as result:
                        result.write(str(self.counts(source)))



def main():
    counter = Tagger()
    counter.count_all_texts()

if __name__ == "__main__":
    main()
