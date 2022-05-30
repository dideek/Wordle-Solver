from main import check_conditions
from main import load_allowed_guesses

def reduce(guess, colors, words):
    space = [];
    for word in words:
        if fits_rules(guess, colors, word):
            space.append(word)
    return space


def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

# xd = load_allowed_guesses()
# xd2 = reduce('ready',[0,0,1,0,0],xd)
# print(xd2)
# print(len(xd2)/len(xd))
