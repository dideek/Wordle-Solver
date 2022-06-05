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

#=========WCZYTYWANIE=========
#Wczytuje Look-Up-Table | full - duża lista
def load_LUT(full=False):
    path = './data/data.pkl' if not full else './data/data_full.pkl'
    with open(path,'rb') as file:
        LUT = pickle.load(file)
        print("loaded")
        return LUT

#Wczytuje liste słow | full - duża lista
def load_words(full=False):
    filename='./data/allowed_words.txt' if full else './data/possible_words.txt'
    file = open(filename, 'r')
    temp = file.read().splitlines()
    return temp

#Oblicza częstotliwość każdej litery w liście słów
def load_letter_distribution(words):
    letters={x: 0 for x in string.ascii_lowercase}
    for word in words:
        for letter in word:
            letters[letter] += 1
    return letters

#=========KOLORY=========
#Zwraca liste słów które dalej są możliwe
def reduce(guess, colors, words):
    return [word for word in words if colors == LUT[word][guess]]

#NIEUŻYWANE | Mamy od tego LUT
#Sprawdza czy słowo jest legalne po danej próbie
def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

#Sprawdza czy wygraliśmy
def check_win_condition(colors):
    return colors == 0b1111111111

#Sprawdza dla strzału czy są zielone pozycje
def check_exact_position(answer_word, input_word):
    colors = 0;

    # Bitmapa dla zielonych kolorów
    for i in range(WORD_LENGTH):
        if answer_word[i] == input_word[i]:
            colors += 3
        colors *= 4
    colors//=4

    return colors

#Sprawdza dla strzału żółte pozycje
def check_presence_condition(answer_word, input_word):
    colors = 0
    tmp_answer_word = list(answer_word)

    # Bitmapa dla żółtych kolorów
    for i in range(WORD_LENGTH):
        if input_word[i] in tmp_answer_word:
            colors += 1
            tmp_answer_word.remove(input_word[i])
        colors *= 4
    colors//=4

    return colors

#Łączy poprzednie dwie funkcje i liczy kolory
def check_conditions(answer_word, input_word):
    exact_position_colors = check_exact_position(answer_word, input_word)
    presence_colors = check_presence_condition(answer_word, input_word)

    final_colors = exact_position_colors | presence_colors

    return final_colors

#0b0001110000 ==> [0,1,3,0,0]
def colors2table(color):
    ret = [0,0,0,0,0]
    for i in reversed(range(WORD_LENGTH)):
        ret[i]=color%4
        color//=4

    return ret

#[0,1,3,0,0] ==> 0b0001110000
def table2color(table):
    colors = 0
    for item in table:
        colors += item
        colors*=4
    colors//=4

    return colors

#=========ENTROPIA=========
#Liczy entropie słowa
def get_entropy(guess,words):
    list = [len(reduce(guess,color,words))/len(words) for color in all_colors]

    # list = []
    # for color in all_colors:
    #     new_words = reduce(guess,color,words)
    #     prob = len(new_words)/len(words)
    #     list.append(prob)

    #print("|= " + guess)
    return (guess, entropy(list, base=2))

def get_entropy_2_layer(guess, words):
    list = [reduce(guess,color,words) for color in all_colors]
    ent1 = entropy([len(x)/len(words) for x in list], base=2)
    ent2s = {x: (0,0) for x in words}
    for words2 in list:
        for word2 in words2:
            _, ent2 = get_entropy(word2, words2)
            a,b = ent2s[word2]
            ent2s[word2] = (a+ent2, b+1)
    tmp = [(a,b/c) for a,(b,c) in ent2s.items()]
    best = max(tmp, key=itemgetter(1))
    print(guess, ent1+best[1])
    return (guess, ent1+best[1])

#Szuka słowa z maksymalną entropią | Używa wątków
def find_best_guess(words):
    entropies = []
    with mp.Pool(mp.cpu_count()) as pool:
        entropies = pool.starmap(get_entropy, zip(words, repeat(words)))

    best = max(entropies, key=itemgetter(1))

    return best

def find_best_guess_2_layer(words):
    entropies = []
    with mp.Pool(mp.cpu_count()) as pool:
        entropies = pool.starmap(get_entropy_2_layer, zip(words, repeat(words)))

    best = max(entropies, key=itemgetter(1))

    return best

#=========INNE=========
def order_by_letters(words):
    points={}
    for word in words:
        suma=0
        for letter in set(word):
            suma+=letters[letter]
        points[word]=suma
    sorted_words = dict(reversed(sorted(points.items(), key=lambda item: item[1])))
    return list(sorted_words.keys())

#Po prostu średnia ważona zaokrąglona do `rounding`
def weighted_average(distribution, weights, rounding):
    return round(sum([distribution[i]*weights[i] for i in range(len(distribution))])/sum(weights), rounding)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

#|||||||||||||||||||||
#=#=#=#=#MAIN#=#=#=#=#
#|||||||||||||||||||||

all_colors = [table2color(x) for x in list(product([3,1,0],repeat=5))]

LUT = load_LUT()
_words = load_words()
letters = load_letter_distribution(_words)

if __name__ == '__main__':
    # t1 = time.time()
    #
    words = load_words()
    # # (guess, e) = find_best_guess(words)
    # (guess,e) = find_best_guess_2_layer(words)
    #
    # t2 = time.time()
    # print(t2-t1)
    # print(guess + " : " + str(e))
    print(get_entropy_2_layer("tares",words))
