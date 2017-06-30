import csv
import unicodedata

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

input_file = csv.DictReader(open("Liz'sTableauMDSStuff/tableaudata/characteristics_split.csv"))

for row in input_file:
   keyTup = (row["play"],row["character"])
   valList = []
   valList.append(row["gender"])
   valList.append(row["role"])
   valList.append(row["genre"])
   characterDict[keyTup]=valList

another_file=csv.DictReader(open("tagging/phonemefreq/tableauVersion.csv"))

with open("tableauwCharacteristics",'a') as dest:
   for row in another_file:
      keyTup = (row["play"],row["char"])
      val = row["phoneme"]
      otherDict[keyTup] = val

      info = (characterDict[keyTup])
      dest.write(str(str(keyTup[0])+","+ str(keyTup[1])+","+val+","+str(info[0])+","+
      str(info[1])+","+str(info[2])+"\n"))


'''def normalize_caseless(text):
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
