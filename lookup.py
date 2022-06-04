from utils import *
import pickle
import sys

#Te 2 funckje tworzą lookup table
#jeśli argv[1] == 'true' to generują długą liste
def compare_to_all_words(guess,words):
    return {word: check_conditions(guess, word) for word in words}

def get_LUT(words):
    return {word: compare_to_all_words(word, words) for word in words}

if __name__ == '__main__':

    if len(sys.argv)>1 and sys.argv[1]=='true':
        words = load_words(full=True)
        data = get_LUT(words)
        path = './data/data_full.pkl'
    else:
        words = load_words()
        data = get_LUT(words)
        path = './data/data.pkl'


    with open(path,'wb') as file:
        pickle.dump(data,file)


    print("Generating finished")
