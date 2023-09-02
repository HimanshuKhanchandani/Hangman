import collections
import re

def join_no_double_counting(word_list):
    """
    This function joins the list of strings in word_list while only keeping unique occurrences of different letters. 
    So it does not overcount the frequency of letters if they appear multiple times in the same word. 
    """
    joined_string = ""
    for word in word_list:
        occured = {}
        for let in word:
            if let in occured:
                continue
            else:
                joined_string += let
                occured[let] = 1
    return joined_string

def guess(dict_of_words, current_dictionary, guessed_letters, word): # word input example: "_ p p _ e "
    ###############################################
    # Replace with your own "guess" function here #
    ###############################################

    
    
    # Making lists of letters that the target word definitely does not contain or definitely contains. 
    excluded_letters = []
    included_letters = {}
    for letter in guessed_letters:
        if letter not in word:
            excluded_letters.append(letter)
        else:
            included_letters[letter] = collections.Counter(word)[letter]
    
    # clean the word so that we strip away the space characters
    # replace "_" with "." as "." indicates any character in regular expressions
    
    clean_word = word[::2].replace("_",".")
    
    # find length of passed word
    len_word = len(clean_word)
    
    # grab current dictionary of possible words from self object, initialize new possible words dictionary to empty
    current_dictionary = current_dictionary
    new_dictionary = []
    
    """
    iterate through all of the words in the old plausible dictionary that match the masked string 
    while excluding the words that contain excluded letters. This is number 2 in the attached file. 
    I allow words containing excluded letters for small words, because there are far less exact matches 
    for small words. 
    """
    

    for dict_word in current_dictionary:
        # continue if the word is not of the appropriate length
        if len(dict_word) != len_word:
            continue
        # breakdown keeps track of if the word contains one of the excluded letters. 
        breakdown = 0    
        # if dictionary word is a possible match then add it to the current dictionary
        if re.match(clean_word,dict_word):
            for lett in excluded_letters:
                if lett in dict_word:
                    breakdown = 1
                    break
            if breakdown == 0:
                new_dictionary.append(dict_word)
            elif (len(clean_word) <= 4) and (len(included_letters) > 0):
                new_dictionary.append(dict_word)
                
   

    # overwrite old possible words dictionary with updated version
    current_dictionary = new_dictionary

    # count occurrence of all characters in possible word matches
    full_dict_string = join_no_double_counting(new_dictionary)
    c = collections.Counter(full_dict_string)
    sorted_letter_count = c.most_common()                   
    
    guess_letter = '!'
    
    # return most frequently occurring letter in all possible words that hasn't been guessed yet
    for letter,instance_count in sorted_letter_count:
        if letter not in guessed_letters:
            # To avoid overfitting, we only use it if its is frequency is not too small. 
            if instance_count > collections.Counter(clean_word)['.']:
                guess_letter = letter
                break
            else:
                break
    
    """
    If we fail to find a new letter, use a different strategy, that is number 3 in the attached file.
    Here we find words in the dictionary that contain the masked string as a substring and do not contain
    excluded letters. So we do not impose the length constaint. 
    """
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:
            breakdown = 0    
        # if dictionary word is a possible match then add it to the current dictionary
            if re.search(clean_word,dict_word):
                for lett in excluded_letters:
                    if lett in dict_word:
                        breakdown = 1
                        break
                if breakdown == 0:
                    new_dictionary.append(dict_word) 
            
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                # This is again to avoid overfitting, I only pick a letter if its frequency is not too small. 
                if len(clean_word) > 6:
                    if instance_count > collections.Counter(clean_word)['.']:
                        guess_letter = letter
                        break
                    else:
                        break
                else:
                    guess_letter = letter
                    break   

    """
    If we still don't have a new guess, we repeat the above but allowing words that may contain the excluded letters
    This is number 4 in the attached pdf. 
    """
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:  
            if re.search(clean_word,dict_word):
                new_dictionary.append(dict_word)
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                if len(clean_word) > 6:
                    if instance_count > collections.Counter(clean_word)['.']:
                        guess_letter = letter
                        break
                    else:
                        break
                else:
                    guess_letter = letter
                    break   
    """
    If everything above fails, we form new words by removing one guessed letter at a time from the clean_word.
    I then find words from the dictionary that match any of these new words and guess a letter based on frequency
    from these words. This is number 5 in the attached pdf. 
    """


    
    if guess_letter == '!':
        new_dictionary = []
        for i in range(len(clean_word)):
            # Only removing letters that have been already guessed. 
            if clean_word[i] == '.':
                continue
            else:
                # forming a new word by removing ith letter
                new_word = clean_word[:i]  + '.' + clean_word[i + 1:]
                for dict_word in dict_of_words:
                    if re.search(new_word, dict_word):
                        new_dictionary.append(dict_word)
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                if len(clean_word) > 6:
                    if instance_count > collections.Counter(clean_word)['.']:
                        guess_letter = letter
                        break
                    else:
                        break
                else:
                    guess_letter = letter
                    break   
    
    
    """
    We now separate out guessed substrings from the clean_word that are actual words in the dictionary,
    and find words in the dictionary that contain the leftover masked string. We then make a guess based 
    on these words in the dictionary. It helps guessing composites like "overrate". 
    This is number 6 on the attached file, and still is a form a partial matching. 
    """
    
    
    if guess_letter == '!':
        # creating a new list of masked strings by separating out guessed words. 
        sub_clean_words = []
        for dict_word in dict_of_words:
            # checking if dict_word is contained in the clean_word
            if (len(dict_word) >=2) and (dict_word in clean_word):
                new_word = clean_word.replace(dict_word, "")
                sub_clean_words.append(new_word)
        # if we have any masked strings in this list, we need to form a new_dictionary of words that match these. 
        if len(sub_clean_words) > 0:
            new_dictionary = []
            for sub_word in sub_clean_words:
                for dict_word in dict_of_words:
                    if re.search(sub_word, dict_word):
                        new_dictionary.append(dict_word)
        
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break          
    
    
    
    """
    In the next step, we just consider all the words that contains all the included letters with the correct
    frequency, and do not contain the excluded letters. This is number 7 on the attached file. 
    """
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:
            # breakdown keeps track of whether the word may be added to the new_dictionary or not. 
            breakdown = 0
            for lett in excluded_letters:
                if lett in dict_word:
                    breakdown = 1
                    break
            for lett in included_letters:
                if lett not in dict_word:
                    breakdown = 1
                    break
                # making sure that the frequencies of all the included letters match up
                elif included_letters[lett] != collections.Counter(dict_word)[lett]:
                    breakdown = 1
                    break
            if breakdown == 0:
                new_dictionary.append(dict_word)
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
    
    # This is the same as above, except we don't care about excluded letters and only match frequencies of included. 
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:
            breakdown = 0
            for lett in included_letters:
                if lett not in dict_word:
                    breakdown = 1
                    break
                elif included_letters[lett] != collections.Counter(dict_word)[lett]:
                    breakdown = 1
                    break
            if breakdown == 0:
                new_dictionary.append(dict_word)
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
    
    # This is again the same as above, but we only care about the letter with highest frequency. 
    
    if guess_letter == '!':
        new_dictionary = []
        included_max = max(included_letters.items(), key = operator.itemgetter(1))[0]
        for dict_word in dict_of_words:
            if included_max not in dict_word:
                continue
            elif included_letters[included_max] != collections.Counter(dict_word)[included_max]:
                continue
            else:
                new_dictionary.append(dict_word)
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
     
    """
    It is quite rare to get here, but if we still don't have a new guessed letter, we just include all the 
    words that include the incuded letters and exclude the excluded letters. This is number 8 on the file. 
    """
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:
            breakdown = 0
            for lett in included_letters:
                if lett not in dict_word:
                    breakdown = 1
                    break
            for lett in excluded_letters:
                if lett in dict_word:
                    breakdown = 1
                    break
            if breakdown == 0:
                new_dictionary.append(dict_word)
    
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
    
    # If we still haven't succeded, we just include all the words with the correct length. 
    
    if guess_letter == '!':
        new_dictionary = []
        for dict_word in dict_of_words:
            if len(dict_word) == len(clean_word):
                new_dictionary.append(dict_word)
    
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
    
    # If we still fail to find a new letter, just include all the words with the same first known letter. 
    
    if guess_letter == '!':
        new_dictionary = []
        for i in range(len(clean_word)):
            if clean_word[i] == '.':
                continue
            else:
                for dict_word in dict_of_words:
                    if dict_word[i] == clean_word[i]:
                        new_dictionary.append(dict_word)
                
                break
        # count occurrence of all characters in possible word matches
        full_dict_string = join_no_double_counting(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()    
    
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break   
    
    
    # Finally if still no word matches in training dictionary, default back to ordering of full dictionary
    if guess_letter == '!':
        sorted_letter_count = dict_of_words_common_letter_sorted
        for letter,instance_count in sorted_letter_count:
            if letter not in guessed_letters:
                guess_letter = letter
                break            
    
    return guess_letter