''' 
   sampleCrystalText.py 
      a program to sample 200 lines of crystaltxt
      to document variations in the txt
'''

import random

lineNumbers = random.sample(range(1,20042),200)

with open("crystal_text.txt", 'r') as source:
    with open ("crystalLines.txt",'a') as dest:
       i = 0
       mlines = 0
       abbrlines = 0
       namelines = 0
       for line in source:
           i = i+1
           if i in lineNumbers:
               dest.write(line)
           if " m " in line:
               mlines +=1 
           if " abbr " in line:
               abbrlines +=1 
           if "[name]" in line:
               namelines +=1
       print (mlines)
       print (abbrlines)
       print (namelines)