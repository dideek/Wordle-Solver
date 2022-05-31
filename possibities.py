from main import check_conditions
from main import load_allowed_guesses
from main import table2color

import math
from itertools import product

#Zwraca liste słów które dalej są możliwe
def reduce(guess, colors, words):
    space = [];
    for word in words:
        if fits_rules(guess, colors, word):
            space.append(word)
    return space

#Sprawdza czy słowo jest legalne po danej próbie
def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

#Liczy entropie słowa -- WIP
def get_entropy(guess,words):
    all_lists = list(product([3,1,0],repeat=5));
    all_colors = [table2color(x) for x in all_lists]
    sum = 0
    for color in all_colors:
        new_words = reduce(guess,color,words)
        prob = len(new_words)/len(words)
        if (prob == 0):
            continue
        bits = math.log2(1/prob)
        sum += prob * bits
    return sum




xd = load_allowed_guesses()
f = get_entropy("crane",xd)
print(f)
