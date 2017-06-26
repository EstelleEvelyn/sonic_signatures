import os
directory = os.fsencode('dest')

numberOfLines = []

for file in os.listdir(directory):
    filename = os.fsencode(file)
    #print (filename)
    if not file is "1H4_Ostler.txt":
       with open(os.path.join(directory,file)) as taco:
           numlines=0
           for line in taco.read():
               print ('hi')
               numlines+=1
           numberOfLines.append(str(str(file) +','+ str(numlines)))

with open("numlines.txt",'a') as result:
    for item in numberOfLines:
        result.write(str(item)+'\n')
        