from main import check_conditions
from main import load_allowed_guesses
import pickle

def compare_to_all_words(guess,words):
    return {word: check_conditions(guess, word) for word in words}

def get_LUT(words):
    return {word: compare_to_all_words(word, words) for word in words}

words = load_allowed_guesses()
data = get_LUT(words)

with open('data.pkl','wb') as file:
    pickle.dump(data,file)


print("Generating finished")
