import os
import math

with open("dest/PP_Austen.txt",'r') as source:
    text = source.readlines()
    phonemeCount = 0
    for line in text:
        line.split()
        for phoneme in line:
            phonemeCount +=1

#path = "/Users/yumetaki/Desktop/sonic_signatures/tagging/counts"
#for fn in os.listdir(path):
    #with open("counts/{}".format(fn), 'r') as source:
with open("counts/PP_Austen_consonants.txt",'r') as source:
   countsArray = []
   typesArray = []
   for line in source:
      currentline = line.split(",")
      type = currentline[0]
      count = int(currentline[1])
      countsArray.append(count)
      typesArray.append(type)
   '''sum = 0
   for count in countsArray:
      sum = sum + int(count)'''
   percentsArray = []
   for count in countsArray:
      #if sum!=0:
      if phonemeCount !=0:
          #percentOfTotal = float(count)/sum
          percentOfTotal = float(count)/phonemeCount
          percentsArray.append(math.ceil((percentOfTotal*100)*100)/100)
      else:
          percentsArray.append(0)
   #print (fn)
   print()
   for percent in percentsArray:
      print (str(percent)+ ("%"))
   #filename = fn.rstrip('.txt')
   filename = "PP_Austen_consonants"
   destination = open("percents/{}_percents.txt".format(filename),'w')
   for i in range(0, len(percentsArray)):
      destination.write(typesArray[i]+ ', ' + str(percentsArray[i])+ ("%")+'\n')
     