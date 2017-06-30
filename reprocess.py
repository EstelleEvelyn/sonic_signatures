from tagging.phonetic_transcriber import Transcriber
from tagging.feature_counter import Counter
from tagging.csv_separator import MPV
from stats.calc_stats import StatCounter
from classifier.manual_classifier import Classifier
from classifier.role_classification import Distinct

import os
import sys
'''
reprocess.py
Estelle Bayer, Summer 2017
A program to run all the necessary data manipulation when changes are made to the
earlier parts of the pipeline
'''
def main():

    if len(sys.argv) == 1:
        new_file = False

    elif sys.argv[1].lower()[0] == "n":
        new_file = True

    else:
        print("Usage: reprocess.py <[n]ew_file> (optional)")
        sys.exit()

    os.chdir("tagging")

    if new_file == True:
        transcr = Transcriber()
        for res_file in os.listdr("/tagging/res"):
            transcr.phonetic_transcript(res_file)
    count = Counter()
    count.count_all_texts()
    mpv = MPV()
    mpv.separate_file()

    os.chdir("../stats")

    stat = StatCounter()
    stat.calc_stats()

    os.chdir("../classifier")
    classif = Classifier()
    classif.classify()
    dist = Distinct()
    dist.write_z_scores()

if __name__ == '__main__':
    main()
