from utils import *
import pickle
import sys

def compare_to_all_words(guess,words):
    return {word: check_conditions(guess, word) for word in words}

def get_LUT(words):
    return {word: compare_to_all_words(word, words) for word in words}

if __name__ == '__main__':

    if len(sys.argv)>1 and sys.argv[1]=='true':
        print("XDDDDD")
    else:
        print(":(")

    raise Exception

    words = load_words()
    data = get_LUT(words)

    with open('data.pkl','wb') as file:
        pickle.dump(data,file)


    print("Generating finished")
