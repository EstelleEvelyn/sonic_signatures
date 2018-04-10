import csv

def combine():
    with open('combinedData.csv', 'w') as destfile:
        with open("features/percentDataOrig.csv", 'r') as featfile:
            feat_reader = csv.reader(featfile)
            for frow in feat_reader:
                filename = frow[0]
                with open("phonemefreq/masterData.csv", 'r') as phonfile:
                    phon_reader = csv.reader(phonfile)
                    for prow in phon_reader:
                        if prow[0] == filename:
                            frow.extend(prow[1:])
                            break
                writer = csv.writer(destfile)
                writer.writerow(frow)

def main():
    combine()

if __name__ == "__main__":
    main()
