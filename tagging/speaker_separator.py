import re
'''
speaker_separator.py
@author Estelle Bayer
A program designed to process transcribed files and separate their text contents
into separate files for distinct speakers
'''
class Separator:
    def __init__(self):
        self.speaker_list = {} #a dictionary of the speakers in a text:their lines

    def find_speakers(self, filename):
        '''
        Given the name of a file in the res folder, determines all of the distinct
        names of speakers in that file using regex
        '''
        with open(filename) as orig_file:
            text = orig_file.read()
            speaker_tags = re.findall("\n.*?:", text)
            for speaker in speaker_tags:
                speaker = speaker[1:-1]
                speaker_exists = False
                for existing_speaker in self.speaker_list:
                    if speaker in existing_speaker:
                        speaker_exists = True
                if not speaker_exists:
                    self.speaker_list[speaker] = []
        return self.speaker_list

    def separate_file(self, filename):
        '''
        Given the name of a file in the res folder, separates the text of that file
        into dictionary entries of the form speaker:speaker's lines
        '''
        self.find_speakers(filename)
        with open(filename) as orig_file:
            raw_text = orig_file.readlines()
            current_speaker = None
            for line in raw_text:
                for speaker in self.speaker_list:
                    if re.match(speaker, line) is not None:
                        current_speaker = speaker
                        line = line.replace(speaker+":", "")
                if current_speaker is not None and line != "\n":
                    line = line.replace("\n", "")
                    self.speaker_list[current_speaker].append(line)
        return self.speaker_list

    def print_new_files(self, filename):
        '''
        Given the name of a file in the res folder, creates new files for every
        speaker in the given file containg all the lines from one individual speaker
        '''
        self.separate_file(filename)
        base_file = filename.lstrip("res/").rstrip(".txt")
        for speaker in self.speaker_list:
            new_file = "res/{0}_{1}.txt".format(base_file, speaker)
            with open(new_file, 'w') as speaker_lines:
                for line in self.speaker_list[speaker]:
                    speaker_lines.write(line)





def main():
    separ = Separator()
    separ.print_new_files("res/presidential_debate.txt")


if __name__ == "__main__":
    main()
