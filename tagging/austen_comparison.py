from nltk_sonic_tagging import Transcriber
from text_classifier import Tagger

def main():
    transcr = Transcriber()
    transcr.phonetic_transcript("PP_Austen")
    tagg = Tagger()
    tagg.count_text("PP_Austen")

if __name__ == "__main__":
    main()
