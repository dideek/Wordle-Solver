from main import *

#"bygbb" ==> 0b0001110000
def string2color(s):
    colors = 0
    guide = {"g":3,"y":1,"b":0}
    for letter in s:
        colors += guide[letter]
        colors*=4
    colors//=4

    return colors

#Podajesz kolory a to mówi co masz wpisać
# b - szary, y - żółty, g - zielony
def play_guide():
    global words, first_guess
    if not first_guess:
        first_guess = find_best_guess(words)[0]

    score = 0
    new_words = words.copy()

    while score < 6:
        guess = find_best_guess(new_words)[0] if score > 0 else first_guess
        print(f"Powinieneś strzelić \"{guess}\"")

        print("Podaj kolory:")
        input_color = input()
        colors = string2color(input_color)
        score += 1
        print_colored_input(guess, colors2table(colors))
        if check_win_condition(colors):
            print()
            return score
        if guess in new_words:
            new_words.remove(guess)
        new_words = reduce(guess, colors, new_words)
        print(f" [{len(new_words)}] words left")

if __name__ == '__main__':
    #first_guess = "raise"
    first_guess = "raise"
    words = load_words()
    while True:
        play_guide()
