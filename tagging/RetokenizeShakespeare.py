from tagging.RegexTokenizer import RegexTokenizer
import urllib
import urllib.request
from bs4 import BeautifulSoup

play_code_list = ['AWW', 'Ant', 'AYL', 'Err', 'Cor', 'Cym', 'Ham', '1H4', '2H4',
                  'H5', '1H6', '2H6', '3H6', 'H8', 'JC', 'Jn', 'Lr', 'LLL', 'Mac',
                  'MM', 'MV', 'Wiv', 'MND', 'Ado', 'Oth', 'Per', 'R2', 'R3', 'Rom',
                  'Shr', 'Tmp', 'Tim', 'Tit', 'Tro', 'TN', 'TGV', 'TNK', 'WT']


def get_character_list(play):
    '''
    Takes a play key for a Shakespeare play and returns a list containing the
    characters in that play
    '''

    base_url = 'http://www.folgerdigitaltexts.org/{}/charText/'
    url = base_url.format(play)

    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    html_data = BeautifulSoup(string_from_server, "html.parser")
    character_list = []
    words_and_chars = html_data.find_all('div')
    for i in range(3, len(words_and_chars)):
        if i % 2 == 1:
            character_list.append(words_and_chars[i].text)
    return character_list


def get_character_text(play, character):
    '''
    Takes the name of a Shakespeare play key and character in that play, and uses the
    Folger API to write that character's text to a file in the res folder
    '''

    character_tag = play + "_" + character

    base_url = 'http://www.folgerdigitaltexts.org/{0}/charText/{1}.html'
    url = base_url.format(play, character_tag)

    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    string_from_server.encode('ascii', 'replace')
    initial_text = BeautifulSoup(string_from_server, 'html.parser')
    for tag in initial_text.findAll('br'):
        tag.replace_with('\n')

    with open('/Users/yumetaki/Desktop/sonic_signatures/tagging/UWTokenizerFiles/{}.txt'.format(character_tag), 'a') as res_file:
        for line in initial_text.find_all('body'):
            write_string = line.text

            print(type(write_string))

            tokenizer = RegexTokenizer()

            new_string = tokenizer.tokenize(write_string)

            print(new_string)
            # TODO try to fix this mapping
            # punctuation_string = string.punctuation.replace("'", "")
            # punctuation_string = string.punctuation.replace("-", "")
            # write_string.translate(str.maketrans("\u2019", "'", punctuation_string))
            # new_string = ""
            # for character in write_string:  # a pretty inefficient loop that only preserves readable text
            #     if character.lower() in "abcdefghijklmnopqrstuvwxyz \n-":
            #         new_string += character
            #     if character == "\u2019":
            #         new_string += "'"
            #res_file.write(str(new_string))


def main():
    for play in play_code_list:
        character_list = get_character_list(play)
        for character in character_list:
            get_character_text(play, character)


if __name__ == "__main__":
    main()
