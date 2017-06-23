import sys
from nltk_sonic_tagging import Transcriber
from text_classifier import Tagger
'''
dynamic_counter.py
@author Estelle Bayer, Summer 2017
A program which takes a file name as a command line argument and calculates the
linguistic feature proportions for that file
'''

def main():

    if len(sys.argv) == 1:
        print("Usage: dynamic_counter.py <file_name>")
        sys.exit()
    else:
        file_name = sys.argv[1]

    transcr = Transcriber()
    transcr.phonetic_transcript(file_name)
    tagg = Tagger()
    tagg.count_all_texts()
    tagg.phoneme_frequency_outputter()

if __name__ == "__main__":
    main()
