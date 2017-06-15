from nltk_sonic_tagging import Transcriber

'''
omission_finder.py
@author Estelle Bayer, Summer 2017
A program to help evaluate the accuracy and speed of our phonetic transcriptions
'''

def main():
    transcriber = Transcriber()
    play_code_list = transcriber.get_play_code_list()
    for play in play_code_list:
        character_list = transcriber.get_character_list(play)
        for character in character_list:
            transcriber.phonetic_transcript(play+"_"+character)

if __name__ == "__main__":
    main()
