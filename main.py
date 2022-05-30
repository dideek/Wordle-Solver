import sys, os
from termcolor import colored, cprint
from wordfreq import word_frequency
os.system("color")


CHANCES = 5
WORD_LENGTH = 5
ANSWER_WORD = "abbey"
GRAY, YELLOW, GREEN = 0, 1, 3

# FORMAT BITMAPY: 5 x 2 bity
# ZIELONY 3 - ŻÓŁTY 1 - SZARY 0
# np GreenYellowGrayGreenGreen = 11 01 00 11 11

def colors2table(color):
    ret = [0,0,0,0,0]
    for i in reversed(range(WORD_LENGTH)):
        ret[i]=color%4
        color//=4

    return ret

def table2color(table):
    colors = 0
    for item in table:
        colors += item
        colors*=4
    colors//=4

    return colors

def map_colors(color_int):
    if color_int == 0: return "GRAY"
    elif color_int == 1: return "YELLOW"
    elif color_int == 3: return "GREEN"


def check_win_condition(colors):
    return colors == 0b1111111111


def check_exact_position(answer_word, input_word):
    colors = 0;

    # Bitmapa dla zielonych kolorów
    for i in range(WORD_LENGTH):
        if answer_word[i] == input_word[i]:
            colors += 3
        colors *= 4
    colors//=4

    return colors

def check_presence_condition(answer_word, input_word):
    colors = 0

    # Bitmapa dla zielonych kolorów
    for i in range(WORD_LENGTH):
        if input_word[i] in answer_word:
            colors += 1
        colors *= 4
    colors//=4

    return colors

def check_conditions(answer_word, input_word):
    exact_position_colors = check_exact_position(answer_word, input_word)
    presence_colors = check_presence_condition(answer_word, input_word)

    final_colors = exact_position_colors | presence_colors

    return final_colors

def print_colored_input(input_word, colors):
    input_word_letters = list(input_word)
    for i in range(WORD_LENGTH):
        if colors[i] == GRAY:
            cprint(input_word_letters[i], "white", "on_red", end="")
        elif colors[i] == GREEN:
            cprint(input_word_letters[i], "white", "on_green", end="")
        else:
            cprint(input_word_letters[i], "white", "on_yellow", end="")
    print()

def run(answer_word):
    print("Dawaj 5 literowe slowo")

    for _ in range(CHANCES):
        input_word = ""
        while True:
            input_word = input()
            if (len(input_word) == WORD_LENGTH):
                break
            else:
                print("Zla dlugosc")

        # sprawdzamy wszystkie warunki
        colors = check_conditions(answer_word, input_word)
        print_colored_input(input_word, colors2table(colors))
        if check_win_condition(colors):
            print("Win")
            return


def load_allowed_guesses():
    filename='allowed_words.txt'
    file = open(filename, 'r')
    temp = file.read().splitlines()
    return temp

def assign_frequencies():
    words_assigned={}
    for word in linex:
        probability=word_frequency(word,'en')
        words_assigned[word]=probability
    return words_assigned


if __name__ == "__main__":
    run(ANSWER_WORD)
