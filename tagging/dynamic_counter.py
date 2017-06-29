import sys
from phonetic_transcribber import Transcriber
from feature_counter import Counter
'''
dynamic_counter.py
@author Estelle Bayer, Summer 2017
A program which takes a file name as a command line argument and calculates the
linguistic feature and phoneme proportions for that file
'''

def main():

    if len(sys.argv) == 1:
        print("Usage: dynamic_counter.py <file_name>")
        sys.exit()
    else:
        file_name = sys.argv[1]

    transcr = Transcriber()
    transcr.phonetic_transcript(file_name)
    counter = Counter()
    counter.count_all_texts()
    counter.phoneme_frequency_outputter()

if __name__ == "__main__":
    main()
