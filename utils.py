import multiprocessing as mp

import math
import time
import pickle
import random
import string

from time import time_ns as xd
from operator import itemgetter
from itertools import product
from itertools import repeat
from scipy.stats import entropy
from statistics import mean

WORD_LENGTH = 5

def load_LUT(full=False):
    path = 'data.pkl' if not full else 'data_full.pkl'
    with open('data.pkl','rb') as file:
        LUT = pickle.load(file)
        print("loaded")
        return LUT

def load_words(full=False):
    filename='allowed_words.txt' if full else 'possible_words.txt'
    file = open(filename, 'r')
    temp = file.read().splitlines()
    return temp

def load_letter_distribution(words):
    letters={x: 0 for x in string.ascii_lowercase}
    for word in words:
        for letter in word:
            letters[letter] += 1
    return letters

def weighted_average(distribution, weights, rounding):
    return round(sum([distribution[i]*weights[i] for i in range(len(distribution))])/sum(weights), rounding)

#Zwraca liste słów które dalej są możliwe
def reduce(guess, colors, words):
    return [word for word in words if colors == LUT[word][guess]]

#Sprawdza czy słowo jest legalne po danej próbie
def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

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

#Liczy entropie słowa -- WIP
def get_entropy(guess,words):
    list = [len(reduce(guess,color,words))/len(words) for color in all_colors]

    # list = []
    # for color in all_colors:
    #     new_words = reduce(guess,color,words)
    #     prob = len(new_words)/len(words)
    #     list.append(prob)

    #print("|= " + guess)
    return (guess, entropy(list, base=2))

def find_best_guess(words):
    entropies = []
    with mp.Pool(mp.cpu_count()) as pool:
        entropies = pool.starmap(get_entropy, zip(words, repeat(words)))

    best = max(entropies, key=itemgetter(1))

    return best

def order_by_letters(words):
    points={}
    for word in words:
        suma=0
        for letter in set(word):
            suma+=letters[letter]
        points[word]=suma
    sorted_words = dict(reversed(sorted(points.items(), key=lambda item: item[1])))
    return list(sorted_words.keys())

#####MAIN######
all_colors = [table2color(x) for x in list(product([3,1,0],repeat=5))]

LUT = load_LUT()
_words = load_words()
letters = load_letter_distribution(_words)

if __name__ == '__main__':
    t1 = time.time()

    words = load_words()
    (guess, e) = find_best_guess(words)

    t2 = time.time()
    print(t2-t1)
    print(guess + " : " + str(e))
