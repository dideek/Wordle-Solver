from main import check_conditions
from main import load_allowed_guesses
from main import table2color
import multiprocessing as mp

import math
import time
from operator import itemgetter
from itertools import product
from itertools import repeat
from scipy.stats import entropy

all_lists = list(product([3,1,0],repeat=5));
all_colors = [table2color(x) for x in all_lists]

#Zwraca liste słów które dalej są możliwe
def reduce(guess, colors, words):
    return [word for word in words if fits_rules(guess,colors,word)]

#Sprawdza czy słowo jest legalne po danej próbie
def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

#Liczy entropie słowa -- WIP
def get_entropy(guess,words):
    list = []
    for color in all_colors:
        new_words = reduce(guess,color,words)
        prob = len(new_words)/len(words)
        list.append(prob)
    sum = entropy(list, base=2)
    print("|= " + guess + " : " + str(sum))
    return (guess, sum)

def find_best_guess(words):
    entropies = []
    with mp.Pool(mp.cpu_count()) as pool:
        entropies = pool.starmap(get_entropy, zip(words, repeat(words)))

    best = max(entropies, key=itemgetter(1))

    return best

words = load_allowed_guesses()
words = words[:1000]
(guess, e) = find_best_guess(words)
print(guess + " : " + str(e))
