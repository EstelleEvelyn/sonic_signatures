

import random
randomnumberlist = []
for x in range(200):
  randomnumberlist.append(random.randint(1,12571))

i = 0
with open("newdict12.txt", 'r+') as testfile:
    with open("sampleofdict.txt", 'a') as samplefile:
        for line in testfile:
            if i in randomnumberlist:
                samplefile.write(line)
            i = i + 1
