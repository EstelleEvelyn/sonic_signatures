import re

class Separator:
    def __init__(self):
        self.speaker_list = {}

    def find_speakers(self, filename):
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
        base_file = filename.lstrip("res/").rstrip(".txt")
        for speaker in self.speaker_list:
            new_file = "res/{0}_{1}.txt".format(speaker, base_file)
            with open(new_file, 'w') as speaker_lines:
                for line in self.speaker_list[speaker]:
                    speaker_lines.write(line)





def main():
    separ = Separator()
    separ.separate_file("res/presidential_debate.txt")
    separ.print_new_files("res/presidential_debate.txt")


if __name__ == "__main__":
    main()
