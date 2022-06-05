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

#NIEUŻYWANE | mamy termcolor
def map_colors(color_int):
    if color_int == 0: return "GRAY"
    elif color_int == 1: return "YELLOW"
    elif color_int == 3: return "GREEN"

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

#mode["entropy"]
def run(answer):
    global words, first_guess
    if not first_guess:
        first_guess = find_best_guess(words)[0]

    score = 0
    new_words = words.copy()

    while score < 6:
        guess = find_best_guess(new_words)[0] if score > 0 else first_guess
        colors = check_conditions(answer, guess)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        if guess in new_words:
            new_words.remove(guess)
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

#mode["random"]
def run_random(answer):
    global words, first_guess

    score = 0
    new_words = words.copy()

    while score < 6:
        guess = random.choice(new_words)
        colors = check_conditions(answer, guess)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        new_words.remove(guess)
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

#mode["common"]
def run_most_common_word(answer):
    global words, first_guess
    new_words = assign_frequencies(words)

    score = 0

    while score < 6:
        guess = new_words[-1]
        colors = check_conditions(answer, guess)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        new_words.remove(guess)
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

#mode["letters"]
def run_best_letter(answer):
    global words
    new_words = order_by_letters(words)
    score = 0

    while score < 6:
        guess = new_words[0]
        colors = check_conditions(answer, guess)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        new_words.remove(guess)
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

#entropia v2
#nie działa bez load_LUT(True) w utils.py
def run_large(answer):
    global words, first_guess
    first_guess = "tares"
    return run(answer)

#Wersja gry z user input
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

#częstotliwość słow w języku angielskim
def assign_frequencies(words):
    words_assigned = {}
    for word in words:
        probability = word_frequency(word, 'en')
        words_assigned[word] = probability
    # define dict

    # open file for writing
    sorted_words = dict(sorted(words_assigned.items(), key=lambda item: item[1]))


    return list(sorted_words.keys())

#coś tam do tej sigmy
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

    #Wybór strategii za pomocą argv[1]
    modes = {
    "entropy":(run, "Wybór maksymalizujący entropię", "entropy.png"),
    "common":(run_most_common_word, "Wybór najczęstszego słowa", "common.png"),
    "random": (run_random, "Losowane słowa", "random.png"),
    "letters": (run_best_letter, "Wybór według najczęstszych liter", "letters.png"),
    "entropy_large": (run_large, "Wybór maksymalizujący entropię w pełnym zestawie\n", "entropy_large.png")
    }

    algorithm,plot_title,plot_name = modes[sys.argv[1]]

    #Tabela wyników
    distribution = [0,0,0,0,0,0,0]

    #Symulacja gry
    for i,answer in enumerate(words):
        print(f"Game {i}")
        score = algorithm(answer)
        if score:
            distribution[score-1] += 1
            print(f"Score: {score} | {distribution}")
        else:
            print("Failed")
            distribution[-1] += 1

    #Dane końcowe
    acceptable_results = [1,2,3,4,5,6,7]
    avg_score = weighted_average(acceptable_results, distribution, 2)
    print(f"Average score: {avg_score} Failures: {distribution[-1]}")

    plt.bar(acceptable_results, distribution)
    plt.title(f"{plot_title} - Średnia: {avg_score} - Porażki: {distribution[-1]}")
    plt.xlabel("Liczba prób")
    plt.ylabel("Liczba wystąpień")
    plt.savefig(f"./graphs/{plot_name}")
    plt.show()
