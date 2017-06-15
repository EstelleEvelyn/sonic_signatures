from nltk_sonic_tagging import Transcriber

'''
text_classifier.py
@authors Estelle Bayer, Liz Nichols, Summer 2017
A program that, given an ARPAbet source file, returns a dictionary containing the
number of occurrences of a handful of linguistic classifications
'''
class Tagger:
    def __init__(self):
        #a dictionary with rudimentary classifications of every phoneme in our source files
        self.consonant_classifier_dictionary = {
            'B':['stop', 'bilabial', 'voiced', 'nonsibilant'],
            'CH':['affricate', 'linguaalveolar', 'voiceless', 'nonsibilant'],
            'D':['stop', 'linguaalveolar', 'voiced', 'nonsibilant'],
            'DH':['fricative', 'linguadental', 'voiced', 'nonsibilant'],
            'F':['fricative', 'labiodental', 'voiceless', 'nonsibilant'],
            'G':['stop', 'linguavelar', 'voiced', 'nonsibilant'],
            'HH':['fricative', 'glottal', 'voiceless', 'nonsibilant'],
            'JH':['affricate', 'linguaalveolar', 'voiced', 'nonsibilant'],
            'K':['stop', 'linguavelar', 'voiceless', 'nonsibilant'],
            'L':['liquid', 'linguaalveolar', 'voiced', 'nonsibilant'],
            'M':['nasal', 'bilabial', 'voiced', 'nonsibilant'],
            'N':['nasal', 'linguaalveolar', 'voiced', 'nonsibilant'],
            'NG':['nasal', 'linguavelar', 'voiced', 'nonsibilant'],
            'P':['stop', 'bilabial', 'voiceless', 'nonsibilant'],
            'R':['liquid', 'linguapalatal', 'voiced', 'nonsibilant'],
            'S':['fricative', 'linguaalveolar', 'voiceless', 'sibilant'],
            'SH':['fricative', 'linguapalatal', 'voiceless', 'sibilant'],
            'T':['stop', 'linguaalveolar', 'voiceless', 'nonsibilant'],
            'TH':['fricative', 'linguadental', 'voiceless', 'nonsibilant'],
            'V':['fricative', 'labiodental', 'voiced', 'nonsibilant'],
            'W':['glide', 'bilabial', 'voiced', 'nonsibilant'],
            'Y':['glide', 'linguapalatal', 'voiced', 'nonsibilant'],
            'Z':['fricative', 'linguaalveolar', 'voiced', 'sibilant'],
            'ZH':['fricative', 'linguapalatal', 'voiced', 'sibilant']
            }
        self.vowel_classifier_dictionary = {
            'AA':['monophthong', 'back'],
            'AE':['monophthong', 'front'],
            'AH':['monophthong', 'central'],
            'AO':['monophthong', 'back'],
            'AW':['diphthong'],
            'AY':['diphthong'],
            'EH':['monophthong', 'front'],
            'ER':['monophthong', 'central'],
            'EY':['diphthong'],
            'IH':['monophthong', 'front'],
            'IY':['monophthong', 'front'],
            'OW':['diphthong'],
            'OY':['diphthong'],
            'UH':['monophthong', 'back'],
            'UW':['monophthong', 'back']
            }


    def consonant_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of consonants
        '''
        return_dict = {'fricative':0, 'affricate':0, 'glide':0, 'nasal':0, 'liquid':0,
                        'stop':0, 'glottal':0, 'linguaalveolar':0, 'linguapalatal':0,
                        'labiodental':0, 'bilabial':0, 'linguavelar':0,'linguadental':0,
                        'voiced':0, 'voiceless':0, 'sibilant':0, 'nonsibilant':0}
        text = read_file.read().split()
        for phoneme in text:
            if phoneme in self.consonant_classifier_dictionary:
                characteristics = self.consonant_classifier_dictionary[phoneme]
                for characteristic in characteristics:
                    return_dict[characteristic] += 1

        return return_dict

    def vowel_counts(self, read_file):
        '''
        Given a file of a phonemes separated by whitespace, returns a dictionary
        of the number of occurrences of a handful of features of vowels
        '''
        return_dict = {'monophthong':0, 'diphthong':0, 'central':0, 'front':0, 'back':0}
        text = read_file.read().split()
        for phoneme in text:
            phoneme = phoneme[:-1]
            if phoneme in self.vowel_classifier_dictionary:
                characteristics = self.vowel_classifier_dictionary[phoneme]
                for characteristic in characteristics:
                    return_dict[characteristic] += 1

        return return_dict

    def count_all_texts(self):
        '''
        For every file in the phonetic transcription folder, writes the counts of
        features to a new file in a counts folder. Entries are separated by newlines
        '''
        transcriber = Transcriber()
        play_code_list = transcriber.get_play_code_list()
        for play in play_code_list:
            character_list = transcriber.get_character_list(play)
            for character in character_list:
                filename = play+"_"+character
                with open ("dest/{}.txt".format(filename), 'r') as source:
                    with open("counts/{}_vowels.txt".format(filename), 'w') as result:
                        vowel_count_dict = self.vowel_counts(source)
                        for item in vowel_count_dict:
                            result.write(item+" , "+str(vowel_count_dict[item])+"\n")
                    with open("counts/{}_consonants.txt".format(filename), 'w') as result:
                        consonant_count_dict = self.consonant_counts(source)
                        for item in consonant_count_dict:
                            result.write(item+" , "+str(consonant_count_dict[item])+"\n")

def main():
    counter = Tagger()
    counter.count_all_texts()

if __name__ == "__main__":
    main()
