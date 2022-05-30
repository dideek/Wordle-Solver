import sys, os
from termcolor import colored, cprint
os.system("color")


CHANCES = 5
WORD_LENGTH = 5
ANSWER_WORD = "abbey"
GRAY, YELLOW, GREEN = 0, 1, 3



def map_colors(color_int):
    if color_int == 0: return "GRAY"
    elif color_int == 1: return "YELLOW"
    elif color_int == 3: return "GREEN"


def check_win_condition(colors):
    is_game_over = True
    for i in range(WORD_LENGTH):
        if colors[i] != GREEN:
            is_game_over = False
            break
    return is_game_over


def check_exact_position(answer_word, input_word):
    answer_word_letters = list(answer_word)
    input_word_letters = list(input_word)

    colors = []

    for i in range(WORD_LENGTH):
        if answer_word_letters[i] == input_word_letters[i]:
            colors.append(GREEN)
        else:
            colors.append(GRAY)

    return colors

def check_presence_condition(answer_word, input_word):
    answer_word_letters = list(answer_word)
    input_word_letters = list(input_word)

    colors = []

    for i in range(WORD_LENGTH):
        if input_word_letters[i] in answer_word_letters:
            colors.append(YELLOW)
        else:
            colors.append(GRAY)

    return colors

def check_conditions(answer_word, input_word):
    exact_position_colors = check_exact_position(answer_word, input_word)
    presence_colors = check_presence_condition(answer_word, input_word)

    final_colors = []
    for i in range(WORD_LENGTH):
        color = exact_position_colors[i] | presence_colors[i]
        final_colors.append(color)

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
        print_colored_input(input_word, colors)
        if check_win_condition(colors):
            print("Win")
            return
        
        
def load_allowed_guesses():
    filename='allowed_words.txt'
    file = open(filename, 'r')
    temp = file.read().splitlines()
    return temp


if __name__ == "__main__":
    run(ANSWER_WORD)

#mama kobasa
