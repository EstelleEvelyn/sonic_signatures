from nltk.corpus import cmudict
import nltk

#nltk_sonic_tagging.py
#@author Estelle Bayer, Summer 2017
#A program using the nltk library to read a source file and write the phonetic
#transcription of the text to a destination file

root = nltk.data.find('/')
transcr = cmudict.dict() #import cmudict
with open('res/hamlet.txt', 'r') as corpus: #source file
    with open('dest/hamlet.txt', 'w') as dest_file: #destination
        corpus_text = corpus.read().lower().split() #normalize
        for word in corpus_text:
            if word in transcr: #TODO find a better way to resolve non-standard words
                phonetic_list = transcr[word][0]
                phonetic_string=""
                for sound in phonetic_list: #this is inefficient
                    phonetic_string = phonetic_string+sound
                dest_file.write(phonetic_string+" ")
