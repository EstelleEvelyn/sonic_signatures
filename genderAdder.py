import csv
import unicodedata
from feature_counter import Counter

''' unimportant script that liz wrote this summer number 3005 '''

playDict = {'All\'s Well That Ends Well':'AWW','Antony and Cleopatra':'Ant','As You Like It':'AYL',
'The Comedy of Errors':'Err','Coriolanus':'Cor','Cymbeline':'Cym','Hamlet':'Ham','Henry IV, Part 1':'1H4',
'Henry IV, Part 2':'2H4','Henry V':'H5','Henry VI, Part 1':'1H6','Henry VI, Part 2':'2H6',
'Henry VI, Part 3':'3H6','Henry VIII':'H8','Julius Caesar':'JC','King John':'Jn',
'King Lear':'Lr','Love\'s Labor\'s Lost':'LLL','Macbeth':'Mac','Measure for Measure':'MM',
'The Merchant of Venice':'MV','The Merry Wives of Windsor':'Wiv','A Midsummer Night\'s Dream':'MND',
'Much Ado About Nothing':'Ado','Othello':'Oth','Pericles':'Per','Richard II':'R2','Richard III':'R3',
'Romeo and Juliet':'Rom','The Taming of the Shrew':'Shr','The Tempest':'Tmp','Timon of Athens':'Tim',
'Titus Andronicus':'Tit','Troilus and Cressida':'Tro','Twelfth Night':'TN',
'Two Gentlemen of Verona':'TGV','Two Noble Kinsmen':'TNK','The Winter\'s Tale':'WT'}

characterDict={}
otherDict={}


counter = Counter()
consonant_dict = counter.consonant_classifier_dictionary
vowel_dict = counter.vowel_classifier_dictionary

input_file = csv.DictReader(open("Liz'sTableauMDSStuff/tableaudata/tableauwCharacteristics.csv"))

for row in input_file:
   phoneme = row["phoneme"]
   attrList=[row["play"],row["character"],row["sex"],row["role"],row["genre"],phoneme]
   if phoneme in consonant_dict:
      with open('consonantsFile.txt','a') as dest:
         attrList += consonant_dict[phoneme]
         dest.write(str(attrList)+"\n")
   elif phoneme in vowel_dict:
      with open ('vowelsFile.txt','a') as dest:
         attrList += vowel_dict[phoneme]
         dest.write(str(attrList)+"\n")
   else:
      print("what?")
         
      
   #if phoneme in consonant dict, write to a consonant file
      #we want play, name, gender, role, phoneme, vowel/consonant, feature... 
   #if phoneme in vowel dict, write to a vowel file
      #we want play, name, gender, role, phoneme, vowel/consonant, feature... 
     # for feature in consonant_dict[phoneme]
         






'''


for row in input_file:
   keyTup = (row["play"],row["character"])
   valTup = (row["phoneme"],row["sex"],row["role"],row["genre"])
   
   characterDict[keyTup]=valTup

another_file=csv.DictReader(open("tagging/phonemefreq/tableauVersion.csv"))

with open("tableauwCharacteristics",'a') as dest:
   for row in another_file:
      keyTup = (row["play"],row["char"])
      val = row["phoneme"]
      otherDict[keyTup] = val
      
      info = (characterDict[keyTup])
      dest.write(str(str(keyTup[0])+","+ str(keyTup[1])+","+val+","+str(info[0])+","+
      str(info[1])+","+str(info[2])+"\n"))


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())

for row in input_file:
   play = row["play"]
   if play in playDict:
       playcode = playDict[play]
       #print(play, playcode)
   tup=(playcode,normalize_caseless(row["character"]))
   print(tup)
   characterDict[tup] = row["gender"]

with open("mdsGendered.txt",'a') as dest:

   mdsFile = csv.DictReader(open("namesPlayCodes.csv"))
   notInDict = 0
   for row in mdsFile:
      tup = (row["play"],normalize_caseless(row["character"]))
      #print(tup)
      if tup in characterDict:
         #print(tup)
         dest.write(tup[0]+','+tup[1]+','+row["x"]+','+row["y"]+','+characterDict[tup]+'\n')
      else:
         #print ("not in character Dict")
         print (tup)
         notInDict +=1
   print (notInDict)
'''         
   
   
   
