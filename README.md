# Hangman
### Algorithm to play Hangman. 
In this project, I write an algorithm to guess the next word in the Hangman game, given the current state of the board, and the guessed letters so far. The version I am playing is the one where we lose the game after 6 incorrect guesses. The guess_function.py file contains details on how the algorithm guesses the next word. The details of hthe guess function are given below. 

### Details of the guess_function
I will outline a series of steps on how to guess the next letter such that the probability that it appears in the word conditional on everything we know about the board is highest. For all the points mentioned here, I will highlight in the python file where the corresponding code is. The basic idea is to look for all the words in the training dictionary that closely match the word we are trying to guess. To do that, we make a list of all the words that match the masked string(i.e with the correctly guessed letters filled in, so a..le for apple once we correctly guess a l and e).  Then find the frequency of occurence of various letters in those words, and guess the letter with the highes frequency as the next letter. 
1. First of all, to count the frequency of letters in a given a list of words, I define a function to join different words together into a big string while only counting every
letter in the word once. So that if a letter appears more than once in a given word, we still only want to count
it once. We care about how many different words it appears in, so when we guess it, we cover most
possible words. 
1. Then I make a list of words that match the masked string but do not contain the excluded
letters (the failed guesses so far). I then guess a letter based on frequencies obtained from this list.
However, to avoid overfitting, I only guess a letter that appears in more than a certain number of words
(number of blanks left).
3. If the above strategy fails to guess a letter (there are not enough words that match the masked string),
I relax it a little bit to find words that contain masked string as a substring (not imposing the length
constraint) while still not containing excluded letters.
4. If that still does not work, I allow words that may contain excluded letters, but also contain the masked
string as a substring.
5. If we still don’t arrive at a new guess, I perform partial matching of the masked string. I obtain new
words from the masked string by removing one letter at a time and look for words that contain these
new masked words as a substring.
6. Now, there is possibility that the word we are trying to guess is composed of two words. If we are in a
situation where we already guessed one of those, we may want to focus on the other one. For example,
if we have ”overr.te”, it may be helpful to focus just on ”r.te”. As part of this strategy, I check if there
are any such words that can be separated from the guessed word. If so, I then form a new dictionary
which match the left over masked string. I base my prediction on this new dictionary. This is still a
form of partial pattern matching.
7. If we still don’t have a new letter, We just include all the words that contain all the included letters
(correct guesses so far) with the exact same frequencies as the word to guess, while not containing any
of the excluded letters. If this becomes too restrictive, we simply relax the excluded constraint, or just
focus on the most frequent letter amongst the guessed letters.
8. It is rare that we still won’t have a new guessed letter. But if we find ourselves in such a situation, we
can just use all the words that contain the included letters and not the excluded letters. Or just include
all the words with the correct length or the first known letter.
9. In all the cases I looked, the steps above successfully guess a new letter. But if that were to not happen,
the algorithm will revert to the frequencies in the full dictionary to guess the next letter


 The dictionary of words comes from this https://github.com/dwyl/english-words. I took these words and randomly split into a 50-50 training and a test set. 
