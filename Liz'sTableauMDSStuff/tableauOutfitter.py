'''for each play
for each character
for each phoneme
write a line to a file that contains
play
character
phoneme'''


from phonetic_transcribber import Transcriber



def main():
    
    transcriber = Transcriber()
    
    
    play_code_list = transcriber.get_play_code_list()
    for play in play_code_list:
        character_list = transcriber.get_character_list(play)
        for character in character_list:
            filename = play+"_"+character
            tableauOutfitter(filename)

def tableauOutfitter(filename):
   
   phonemeList = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
       'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
       'UH','UW','V','W','Y','Z','ZH']
   
   splitName = filename.split('_')
   
   play = splitName[0]
   character = splitName[1]
   
   with open("dest/{}.txt".format(filename), 'r') as source:
       with open("phonemefreq/tableauVersion.txt",'a') as destination:
           text = source.read().split()
           for phoneme in text:
               if phoneme[-1] in '0123456789':
                   phoneme = phoneme[:-1]
               if phoneme in phonemeList:
                   #print(phoneme)
                   destination.write(play+','+character+','+ phoneme + '\n')

main()

                            
                   
