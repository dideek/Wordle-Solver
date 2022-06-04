import sys, os
from termcolor import colored, cprint
from wordfreq import word_frequency
import matplotlib.pyplot as plt

from utils import *

os.system("color")

CHANCES = 5
WORD_LENGTH = 5
#ANSWER_WORD = "steal"
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
    tmp_answer_word = list(answer_word)

    # Bitmapa dla zielonych kolorów
    for i in range(WORD_LENGTH):
        if input_word[i] in tmp_answer_word:
            colors += 1
            tmp_answer_word.remove(input_word[i])
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
    #print()

def run(answer):
    global words, first_guess
    if not first_guess:
        first_guess = find_best_guess(words)[0]

    score = 1
    colors = check_conditions(answer, first_guess)
    print_colored_input(first_guess, colors2table(colors))
    if check_win_condition(colors):
        return score
    new_words = reduce(first_guess, colors, words)
    print(f" [{len(new_words)}] words left")

    while score < 6:
        guess = find_best_guess(new_words)[0]
        colors = check_conditions(answer, guess)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

def play(answer_word):
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


def load_words(all_words=False):
    filename='allowed_words.txt' if all_words else 'possible_words.txt'
    file = open(filename, 'r')
    temp = file.read().splitlines()
    return temp

def assign_frequencies():
    words_assigned = {}
    for word in linex:
        probability = word_frequency(word, 'en')
        words_assigned[word] = probability
    # define dict

    # open file for writing
    sorted_words = dict(sorted(words_assigned.items(), key=lambda item: item[1]))


    return sorted_words


def interpolate():
    increment = 7/  len(sorted_words) # tą 7 mozna mzieniac
    i = 0
    interpolated_words = {}
    for word in sorted_words:
        x = -8 + increment * i*2 #  Tu -8 i i*2 tez mozna zmieniac zeby modyfikowac predkosc wzrostu grafu / przesunięcie wartości lewo prawo
        interpolated_words[word] = x
        i+=1
    for word in interpolated_words:
        x=1/(1+math.e**-interpolated_words[word])
        interpolated_words[word]=x
    #DEBUG
    #values = interpolated_words.values()
    # open file for writing
    #f = open("interpolated_twice.txt", "w")

    # write file
    #f.write(str(interpolated_words))

    # close file
    #f.close()
    #plt.plot(values)
    #plt.show()
    return interpolated_words

if __name__ == '__main__':
    first_guess = 'raise'
    words = load_words()

    distribution = [0,0,0,0,0,0]
    fails = 0

    for i,answer in enumerate(words):
        break
        print(f"Game {i}")
        score = run(answer)
        if score:
            distribution[score-1] += 1
            print(f"Score: {score} | {distribution}")
        else:
            print("Failed")
            fails += 1

    acceptable_results = [1,2,3,4,5,6]
    avg_score = weighted_average(acceptable_results, distribution)
    print(f"Average score: {avg_score} Failures: {fails}")

    plt.bar(acceptable_results, distribution)
    plt.title(f"Dojebana metoda - srednia {avg_score}")
    plt.xlabel("Liczba prob")
    plt.ylabel("Liczba wystapien")
    plt.savefig("dojebanametoda.png")
    plt.show()