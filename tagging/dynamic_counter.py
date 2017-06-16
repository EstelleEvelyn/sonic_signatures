import sys
from nltk_sonic_tagging import Transcriber
from text_classifier import Tagger

def main():

    if len(sys.argv) == 1:
		print("Usage: dynamic_counter.py <file_name>")
    else:
        file_name = sys.argv[1]
    transcr = Transcriber()
    transcr.phonetic_transcript(file_name)
    tagg = Tagger()
    tagg.count_text(file_name)

if __name__ == "__main__":
    main()
