import guess_function

def play_game(word, train_dictionary, verbose = False):
    incorrect_guesses = 0
    current_word = ""
    for i in range(len(word) - 1):
        current_word += "_ "
    current_word += "_"
    guessed_letters = []
    while (incorrect_guesses < 6) or (current_word[::2] != word):
        current_guess = guess_function.guess(train_dictionary, train_dictionary, guessed_letters, current_word)
        guessed_letters += [current_guess]
        if current_guess in word:
            for i in range(len(word) - 1):
                if word[i] == current_guess:
                    current_word = current_word[0:2*i] + current_guess + current_word[2*i + 1:]
            if word[len(word) - 1] == current_guess:
                current_word = current_word[0:2*(len(word) - 1)] + current_guess
        else:
            incorrect_guesses += 1
        if verbose:
            print('Guessing ', current_guess, 'current state is ', current_word)
            
    
    if incorrect_guesses == 6:
        print('The algorithm lost')
        return False
    elif current_word[::2] == word:
        print('The algorithm won')
        return True
