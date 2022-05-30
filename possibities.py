from main import check_conditions
from main import load_allowed_guesses
from main import table2color
from itertools import product

def reduce(guess, colors, words):
    space = [];
    for word in words:
        if fits_rules(guess, colors, word):
            space.append(word)
    return space


def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

def get_entropy(guess,words):
    all_lists = list(product([3,1,0],repeat=5));
    all_colors = [table2color(x) for x in all_lists]
    sum = 0
    for color in all_colors:
        nl = reduce(guess,color,words)
        tmp = len(nl)/len(words)
        print(tmp)
        sum += tmp
    print(sum)

xd = load_allowed_guesses()
get_entropy("kurwa",xd)
