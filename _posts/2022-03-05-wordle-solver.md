---
title: Solving Wordle using Python and Basic Frequency Analysis
excerpt: A quick writeup on a simple way I approached solving Wordle with Python and letter frequency analysis. 
tags: programming fun
author: rms
---

## What's Wordle?

{:refdef: style="text-align: center;"}
![Wordle](https://starwarsfan2099.github.io/public/2022-03-05/wordle.jpg){:.shadow}
{: refdef}

Wordle is a small online game that has blown up in popularity recently. It's premise is simple, you have six tries to guess a five letter word. I'm going to call this the target word. Each guess reveals information about the target word. If a letter you guessed is at the same place in the target word, it's square in the grid is colored green. If the letter is in the target word but it in the incorrect place, the square is colored yellow. And finally, if the letter is not in the target word the square is blank with no color. 

In the example image above, the first word I guessed was *beach*. "B" is colored green, so the target word starts with a "B". "E" is colored yellow, so the letter "E" is in the word, but is not the second letter in the word. "A", "C", and "H" are not found anywhere in the target word. The next word I guess is *brief*. "B" is the first letter and the letter "E" is in the word and not in the second place. I got lucky and go too more letters that are in the correct space: "R" and "I". The "E" is yellow, so the only other place it can be is the last place. Now we only have to guess one more letter. And from the other guesses we know that "B", "E", "A", "C", "H", and "F" are not letters that can be in the next to last place. My final guess was the word *brine*. All the squares are green, and that was in fact the target word. 

## Frequency analysis?

Frequency analysis is used to determine the frequency of individual letters in the English language. This is shows us what letters are used more frequently than others, for example, the letter "A" is more common in words than "Z". This can be used for solving a Wordle by guessing the most likely word with the information returned from previous guesses. Thankfully, a frequency analysis of all English letters already exists.

{:refdef: style="text-align: center;"}
![Table](https://starwarsfan2099.github.io/public/2022-03-05/table.jpg){:.shadow}
{: refdef}

Using this information, we can generate a 'score' for each five letter word that is a possible guess or possible Wordle. This score can than be used to determine the *most likely* guess with the given information. Simple really.

## The code
### Wordle Solver class

If you want to see the full source code, it's at the bottom of the post or can be found [here](https://gist.github.com/Starwarsfan2099/600899c8ebbe75e5b3e0bf581c38c5fa). Now, lets walk through the code.

{% highlight python linenos %}
from sys import argv
from time import time

# Wordle Solver class
class WordleSolve:

    def __init__(self, file_name, start_word):

        # Alphabet letters sorted by frequency
        self.letter_freq = ["s", "e", "a", "r", "o", "i", "l", "t", "n", "u", "d", "c", "y", "p", "m", "h", "g", "b", "k", "f", "w", "v", "z", "x", "j", "q"]
        self.letter_freq_value = [46.1, 44.8, 40.5, 30.9, 29.5, 28.1, 25, 24, 21.4, 18.6, 18.1, 15.7, 15.4, 14.6, 14.2, 13.3, 11.8, 11.5, 10.2, 7.9, 7.7, 5.2, 2.5, 2.4, 2.1, 0.9]
        self.letter_pairs = ["th", "he", "an", "in", "er", "nd", "re", "ed", "es", "ou", "to", "ha", "en", "ea", "st", "nt", "on", "at", "hi", "as", "it", "ng", "is", "or", "et", "of", "ti", "ar", "te", "se", "me", "sa", "ne", "wa", "ve", "le", "no", "ta", "al", "de", "ot", "so", "dt", "ll", "tt", "el", "ro", "ad", "di", "ew", "ra", "ri", "sh"]
        self.letter_pairs_freq = [33, 30.2, 18.1, 17.9, 16.9, 14.6, 13.3, 12.6, 11.5, 11.5, 11.5, 11.4, 11.1, 11, 10.9, 10.6, 10.6, 10.4, 9.7, 9.5, 9.3, 9.2, 8.6, 8.4, 8.3, 8, 7.6, 7.5, 7.5, 7.4, 6.8, 6.7, 6.6, 6.6, 6.5, 6.4, 6, 5.9, 5.7, 5.7, 5.7, 5.7, 5.6, 5.6, 5.6, 5.5, 5.5, 5.2, 5, 5, 5, 5, 5]
        self.target_word = ["_", "_", "_", "_", "_"]
        self.yellow_green_list = []
        self.not_list = []
        self.word_history = []
        self.score_list = []
        self.start_word = start_word

        # Open a list of 5 letter words and save in memory
        word_list_file = open(file_name, "r")
        self.word_list = word_list_file.read().split()
        word_list_file.close()
        self.word_list_total = len(self.word_list)

{% endhighlight %}

First, `argv` is imported for command line arguments and `time` is imported to time the script later on. Next, a class `WordleSolve` is created and inside it is the constructor function `__init__`. In the constructor, several variables are created and initialized. The constructor accepts a file name and the starting word for Wordle. Once in `__Init__`, firstly, two variables to help with letter frequency analysis: `letter_freq`, `letter_freq_value`, `letter_pairs`, and `letter_pairs_freq`. `letter_freq` contains a list of English letters sorted form highest frequency to lowest frequency. `letter_freq_value` contains the actual frequency values from largest value to smallest. `letter_pairs` and `letter_pairs_freq` are the same but for common pairs of letters. Next, some variables that are used later are initilized. `target_word`, `yellow_green_list`, `not_list`, `word_history`, `score_list`, and `start_word`. 

For this program, a word list of five letter words is used. Next, the word list provided is opened and the contents are read and stored in a list. 

{% highlight python linenos %}
    # Print a list of words in a box like Wordle does
    def box(self, words):
        # Box top and bottom
        box_top = "  ___________________ "
        box_spacer  = "  ------------------- "   
        output = box_top
        for word in words:
            output += "\n" + ' | ' +  ' | '.join(list(word)) + ' | ' + "\n" + box_spacer
        return output

    # Get user input
    def get_input(self):
        text = input("Enter results: ")
        input_list = []
        for letter in text:
            input_list.append(letter)
        return input_list
{% endhighlight %}

Next, are two simple hepler functions. One for printing out Wordle guesses in a wordle 'box' and a function for user input. 

{% highlight python linenos %}
    # If we know a letter is or isn't in a word, adjust the word list apropriatly
    def letter_modify(self, letter, remove):
        i = 0
        while i < len(self.word_list):
            if remove:
                if letter in self.word_list[i]:
                    if letter not in self.yellow_green_list:
                        self.word_list.pop(i)
                        self.score_list.pop(i)
                        continue
            if not remove:
                if letter not in self.word_list[i]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            i += 1

    # If we know what place a letter is or isn't, adjust the word list apropriatly
    def letter_place(self, place, letter, remove):
        i = 0
        while i < len(self.word_list):
            if remove:
                if letter in self.word_list[i][place]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            if not remove:
                if letter not in self.word_list[i][place]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            i += 1
{% endhighlight %}

These functions handle modifying the word list after information is received from a guess. `letter_modify` accepts a letter and the boolean `remove`. If `remove` is `True`, any words in the wordlist that contain `letter` are removed from thre list. If `remove` is `False`, Any words that don't have `letter` in the word are removed from the wordlist. For example, if a word is guessed and a letter is blank, that means the letter isn't anywhere in the target word. So, all words containging that letter are removed from the list. Or, if a letter is is definetly in a word, e.g. a yellow blank, `remove` is `False` and all words *without* the letter are removed from the list. `yellow_green_list` is a list of previous letters that have have already been removed from the list. 

`letter_place` is used for green or yellow squares. If a word is guessed and a letter is in a green square, than all words without that letter in that place are removed. So, if `remove` is `True`, all words in the list with `letter` in `place` are removed. If `remove` is `False`, all words in the word list that don't have `letter` in `place` are removed from the list. 

{% highlight python linenos %}
    # Add known letters in the word to a list
    def add_known_letters(self, letter):
        if letter not in self.yellow_green_list:
            self.yellow_green_list.append(letter)

    # Add known letter not in the word to a list
    def add_known_not_letters(self, letter):
        if letter not in self.not_list:
            self.not_list.append(letter)

    # Print a few stats
    def stats(self):
        print("\nWordle: %s" % ' '.join(self.target_word))
        print("Known letters in word: %s" % ' '.join(self.yellow_green_list))
        print("Known letters not in word: %s" % ' '.join(self.not_list))
        print("{0} words remaining, down to {1:.2%} of words.\n".format(len(self.word_list), (len(self.word_list)/self.word_list_total)))
{% endhighlight %}

`add_known_letters` is used to add letters to a list of letters that we know are in the target word. `add_known_not_letters` is used to add letters to a list of list of letetrs that are definetly not in the word. This is for optimization. `stats` just prints out some stats on the current Wordle.

{% highlight python linenos %}
    # Sort word list based on a letter frequency score
    def sort_by_freq(self):
        self.score_list = []
        for word in self.word_list:
            i = 1
            score = 0
            letters = []
            for letter in word:
                # Add to score for top signifigant letters by position
                if i == 1 and letter == "s": score += 11.5
                if i == 2 and letter == "a": score += 12.5
                if i == 3 and letter == "r": score += 11.7
                if i == 4 and letter == "e": score += 12.5  
                if i == 5 and letter == "s": score += 13.1 
                if letter not in letters:
                    # Add the frequency score of a letter to the score.
                    score += float(self.letter_freq_value[self.letter_freq.index(letter)])
                else:
                    # If a letter is in a word more than once, reduce value of any other occurences. Magic number seems freq/5. 
                    score += float(self.letter_freq_value[self.letter_freq.index(letter)])/5
                letters.append(letter)
                i += 1
            # Now, we add a value based upon frequency of common letter pairs. 
            for pair in self.letter_pairs:
                if pair in word:
                    score += float(self.letter_pairs_freq[self.letter_pairs.index(pair)])
            self.score_list.append(score)
        # Sort the list of scores.
        zipped_list = sorted(zip(self.score_list, self.word_list), reverse=True)
        self.word_list = [self.word_list for score_list, self.word_list in zipped_list]
        self.score_list = sorted(self.score_list, reverse=True)
        return zipped_list
{% endhighlight %}

The function `sort_by_freq` is used to sort the wordlist based on a score of the words letter frequency. The function loops over each letter in every word in the wordlist. First, the function checks what position in the word it as at and checks if a certian letter is in that place. For the first letter place, the most common letter is *s*. If *s* is in the first place, it adds to the score. Second, it takes the frequency value of the current lettert and adds it to the score. It aslo chcks if the letter is in the word more than once. To optimize Wordle, words with duplicates of letters are less useful. For each duplicate letter, the freqency is divided by 5 then added to the score. Finally, it checks for common letter pairs and adds to the score based on how many andf what pairs are in the word. This creates a frequency score and is stored in `score_list`. Once each word has a score, the wordlist and score list are zipped and sorted by the score. `word_list` is then sorted and the function returns the `zipped_list`. 

{% highlight python linenos %}
    # Process input and adjust the word list starting with known letters in the target word
    def process_guess(self, input_list, iteration):
        # Known letter and position [Green square]
        i = 0
        for letter in input_list:
            if letter == "g":
                self.add_known_letters(self.word_history[iteration][i])
                self.letter_place(i, self.word_history[iteration][i], False)
                self.target_word[i] = self.word_history[iteration][i]
            i +=1

        # Known letter but not position [Yellow square]
        i = 0
        for letter in input_list:
            if letter == "y":
                self.add_known_letters(self.word_history[iteration][i])
                self.letter_place(i, self.word_history[iteration][i], True)
                self.letter_modify(self.word_history[iteration][i], False)
            i +=1
        
        # Known not a letter in the target word [Blank square]
        i = 0
        for letter in input_list:
            if letter == "b":
                self.letter_modify(self.word_history[iteration][i], True)
                self.add_known_not_letters(self.word_history[iteration][i])
            i += 1
{% endhighlight %}

Next, a function to process a user guess. The function takes `input_list` and `iteration` as arguments. `input_list` is a list of the results after a guess in the form of `bbyygg`. `b` is for a blank square, `y` is for a yellow square, and `g` is for a green square. `iteration` is what guess the user is on. This function loops over the results and makes the appropriate changes to the word list, letter lists, and word history. 

{% highlight python linenos %}
    # Wordle logic for running tests
    def wordle_logic(self, guess, wordle):
        i = 0
        output = []
        for letter in guess:
            if letter == wordle[i]:
                output.append("g")
            elif letter in wordle:
                output.append("y")
            elif letter not in wordle:
                output.append("b")
            else:
                print("Something bad happened.")
            i += 1
        if len(output) != 5:
            print("Something bad happened x2.")
        return output
{% endhighlight %}

And finally, there is a bot function to use for testing optimization and start words. The function takes a `guess` and a `wordle` and returns a string as if a user was playing. (e.g., in the form of `bbyygg`) And that's the end of the Wordle solving class. 

### Using the WordleSolver class

{% highlight python linenos %}
# Automatically play Wordle for testing code, start words, etc.
def play_bot(solver, target_list, start_word, verbose):
    succsess = []
    solver.word_list = []
    word_list_sorted = []
    score_list_sorted = []
    fails = 0
    for word in target_list:
        solver.word_list.append(word)

    # Sort by frequency and backup those values
    scores = solver.sort_by_freq()
    for word in solver.word_list:
        word_list_sorted.append(word)
    for score in solver.score_list:
        score_list_sorted.append(score)

    for wordle in target_list:
        if verbose: print("Wordle: %s" % wordle, end='\r')
        solver.word_list = []
        solver.word_history = []
        solver.yellow_green_list = []
        solver.score_list = [] 

        # Copy the saved frequency values instead of calculating them again
        for word in word_list_sorted:
            solver.word_list.append(word)
        for score in score_list_sorted:
            solver.score_list.append(score)

        i = 0
        for i in range(0, 6):
            if i == 0:
                solver.word_history.append(start_word)
                guess = solver.wordle_logic(start_word, wordle)
            else:
                solver.word_history.append(solver.word_list[0])
                guess = solver.wordle_logic(solver.word_list[0], wordle)
            solver.process_guess(guess, i)
            if ''.join(guess) == "ggggg":
                succsess.append(i + 1)
                break
            if len(solver.word_list) == 1:
                succsess.append(i + 1)
                break
            if i == 5:
                fails += 1
            if solver.word_list[0] in solver.word_history:
                solver.word_list.pop(0)
    count = 0
    for i in succsess:
        count += i
    return count, succsess, fails
{% endhighlight %}

Next, there is function to have a bot 'solve' a Wordle. This is used for testing start words and optimization testing. This function takes a `WordleSolver` class, list of Wordles, starting guess word, and a verbose boolean as input. The code loops over the Wordles in `target_list` and then prints the Wordle if `verbose` is true. Next, since the bot function is passed a single instance of `WordleSolver` but loops over many Wordles, certain variables like `word_list` and `word_history` are reinitialized. This is done to avoid having to reload the wordlist for every Wordle. Then, all of the target Wordles are copied into `word_list`. Then, the wordlist is sorted with `sort_by_freq()`. Then, six guesses are done. If it's the first guess (`i==0`) then the `start_word` is used. Otherwise, it uses the first word in the `word_list`. This is the most likely word based on letter frequency and the list has had any words removed that will not work. The guesses and Wordle are passed to `wordle_logic` which returns the result. The result is processed with `process_guess`. If `wordle_logic` returns `ggggg` or there is only one word left in `word_list`, then the Wordle has been solved! It keeps track of the number of guesses, fails, and succsess and returns them. 

{% highlight python linenos %}
# Using each word in the word list as a Wordle, try to solve it and see what the average number of guesses is
def test():
    start_word = "least"
    successes = []
    fails = 0
    target_list = []
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    for word in solver.word_list:
        target_list.append(word)
    count, successes, fails = play_bot(solver, target_list, start_word, True)
    print("Number of wordles: %s" % len(target_list))
    print("Number of succsess: %s" % len(successes))
    print("Average guesses for successes: %s" % (count/len(successes)))
    print("Fails: %s" % fails)
{% endhighlight %}

Now the `play_bot` function can be used to test the solver with one start word on all possible Wordles! Simply initialize the `WordleSolve` class with a starting guess, and a wordlist, then pick and a Wordle list, pick a verbosity and call `play_bot`. Next, the `test` function simply prints the results of the test. Here is an example of it running:

```
Number of wordles: 2315
Number of succsess: 2302
Average guesses for successes: 3.094265855777585
Fails: 13
Time: 17.315351486206055
```

It's also possible to test all of the possible start words on all possible Wordles to determine what the best start word is.

{% highlight python linenos %}
# Using each word in the word list as a Wordle, try to solve it and see what the average number of guesses is
def test_start_words():
    averages = []
    target_list = []
    start_word_list =[]
    start_word = "least"
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    for word in solver.word_list:
        start_word_list.append(word)
    for word in solver.word_list:
        target_list.append(word)
    for start_word in start_word_list:
        successes = []
        fails = 0
        count, successes, fails = play_bot(solver, target_list, start_word, False)
        averages.append((count/len(successes), start_word))
        print((count/len(successes), start_word), len(successes))
    result = sorted(averages)
    print("The best start word is %s with a average of %f Wordle guesses." % (result[0][1], result[0][0]))

{% endhighlight %}

The function `test_start_words` copies all of the words in `word_list` to a `start_word_list`. Then, it uses the `play_bot` function to test every single starting word and record the results. After that finally finishes, it zips the results and sorts them to see what start word yielded the lowest average number of guesses to solve all Wordles. (**Spoiler:** The best start word with this script is *least*) And finally, there is a function for a user to use the Solver and play on the website.

{% highlight python linenos %}
# Solve a Wordle with a user
def play():
    start_word = "least"
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    solver.stats()
    print("Begin with:")
    scores = solver.sort_by_freq()
    print(solver.box([start_word]))
    solver.word_history.append(start_word)
    i = 0
    for i in range(0, 6):
        user_input = solver.get_input()
        solver.process_guess(user_input[:5], i)
        solver.stats()
        print("Top words:")
        try:
            for x in range(0, 4):
                print("""%s (Freq score: %.2f)""" % (solver.word_list[x], round(solver.score_list[x], 2)))
        except Exception as e:
            pass
        if len(solver.word_list) == 1:
            if ''.join(user_input[:5]) == "ggggg":
                print(solver.box(solver.word_history))
            else:
                print(solver.box(solver.word_history + [solver.word_list[0]]))
            print("Done! Hooray!!")
            exit()
        if solver.word_list[0] in solver.word_history:
            solver.word_list.pop(0)
        print(solver.box(solver.word_history + [solver.word_list[0]]))
        solver.word_history.append(solver.word_list[0])
    print("Oof. Good luck picking final word!")

{% endhighlight %}

This function is similar to the `play_bot` functionality, but the user's input from the website replaces `wordle_logic()`. The stats are also printed as well as the guess history in the ASCII text box. The last bit of the script gives some command line args for different test or playing as a user.

{% highlight python linenos %}
# Main
if __name__ == "__main__":
    startTime = time()
    if len(argv) == 1:
        print("Try again.")
    elif argv[1] == "test":
        test()
    elif argv[1] == "play":
        play()
    elif argv[1] == "test_start_words":
        test_start_words()
    else:
        print("Try again.")
    executionTime = (time() - startTime)
    print('Time: ' + str(executionTime))
{% endhighlight %}

## Full Code

The code can be found [here](https://gist.github.com/Starwarsfan2099/600899c8ebbe75e5b3e0bf581c38c5fa) on GitHub and below:

{% highlight python linenos %}
#!/usr/bin/python3

# Quick and dirty wordle solver
# b is blank square, y is yellow square, g is green square.

from sys import argv
from time import time

# Wordle Solver class
class WordleSolve:

    def __init__(self, file_name, start_word):

        # Alphabet letters sorted by frequency
        self.letter_freq = ["s", "e", "a", "r", "o", "i", "l", "t", "n", "u", "d", "c", "y", "p", "m", "h", "g", "b", "k", "f", "w", "v", "z", "x", "j", "q"]
        self.letter_freq_value = [46.1, 44.8, 40.5, 30.9, 29.5, 28.1, 25, 24, 21.4, 18.6, 18.1, 15.7, 15.4, 14.6, 14.2, 13.3, 11.8, 11.5, 10.2, 7.9, 7.7, 5.2, 2.5, 2.4, 2.1, 0.9]
        self.letter_pairs = ["th", "he", "an", "in", "er", "nd", "re", "ed", "es", "ou", "to", "ha", "en", "ea", "st", "nt", "on", "at", "hi", "as", "it", "ng", "is", "or", "et", "of", "ti", "ar", "te", "se", "me", "sa", "ne", "wa", "ve", "le", "no", "ta", "al", "de", "ot", "so", "dt", "ll", "tt", "el", "ro", "ad", "di", "ew", "ra", "ri", "sh"]
        self.letter_pairs_freq = [33, 30.2, 18.1, 17.9, 16.9, 14.6, 13.3, 12.6, 11.5, 11.5, 11.5, 11.4, 11.1, 11, 10.9, 10.6, 10.6, 10.4, 9.7, 9.5, 9.3, 9.2, 8.6, 8.4, 8.3, 8, 7.6, 7.5, 7.5, 7.4, 6.8, 6.7, 6.6, 6.6, 6.5, 6.4, 6, 5.9, 5.7, 5.7, 5.7, 5.7, 5.6, 5.6, 5.6, 5.5, 5.5, 5.2, 5, 5, 5, 5, 5]
        self.target_word = ["_", "_", "_", "_", "_"]
        self.yellow_green_list = []
        self.not_list = []
        self.word_history = []
        self.score_list = []
        self.start_word = start_word

        # Open a list of 5 letter words and save in memory
        word_list_file = open(file_name, "r")
        self.word_list = word_list_file.read().split()
        word_list_file.close()
        self.word_list_total = len(self.word_list)

    # Print a list of words in a box like Wordle does
    def box(self, words):
        # Box top and bottom
        box_top = "  ___________________ "
        box_spacer  = "  ------------------- "   
        output = box_top
        for word in words:
            output += "\n" + ' | ' +  ' | '.join(list(word)) + ' | ' + "\n" + box_spacer
        return output

    # Get user input
    def get_input(self):
        text = input("Enter results: ")
        input_list = []
        for letter in text:
            input_list.append(letter)
        return input_list

    # If we know a letter is or isn't in a word, adjust the word list apropriatly
    def letter_modify(self, letter, remove):
        i = 0
        while i < len(self.word_list):
            if remove:
                if letter in self.word_list[i]:
                    if letter not in self.yellow_green_list:
                        self.word_list.pop(i)
                        self.score_list.pop(i)
                        continue
            if not remove:
                if letter not in self.word_list[i]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            i += 1

    # If we know what place a letter is or isn't, adjust the word list apropriatly
    def letter_place(self, place, letter, remove):
        i = 0
        while i < len(self.word_list):
            if remove:
                if letter in self.word_list[i][place]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            if not remove:
                if letter not in self.word_list[i][place]:
                    self.word_list.pop(i)
                    self.score_list.pop(i)
                    continue
            i += 1

    # Add known letters in the word to a list
    def add_known_letters(self, letter):
        if letter not in self.yellow_green_list:
            self.yellow_green_list.append(letter)

    # Add known letter not in the word to a list
    def add_known_not_letters(self, letter):
        if letter not in self.not_list:
            self.not_list.append(letter)

    # Print a few stats
    def stats(self):
        print("\nWordle: %s" % ' '.join(self.target_word))
        print("Known letters in word: %s" % ' '.join(self.yellow_green_list))
        print("Known letters not in word: %s" % ' '.join(self.not_list))
        print("{0} words remaining, down to {1:.2%} of words.\n".format(len(self.word_list), (len(self.word_list)/self.word_list_total)))

    # Sort word list based on a letter frequency score
    def sort_by_freq(self):
        self.score_list = []
        for word in self.word_list:
            i = 1
            score = 0
            letters = []
            for letter in word:
                # Add to score for top signifigant letters by position
                if i == 1 and letter == "s": score += 11.5
                if i == 2 and letter == "a": score += 12.5
                if i == 3 and letter == "r": score += 11.7
                if i == 4 and letter == "e": score += 12.5  
                if i == 5 and letter == "s": score += 13.1 
                if letter not in letters:
                    # Add the frequency score of a letter to the score.
                    score += float(self.letter_freq_value[self.letter_freq.index(letter)])
                else:
                    # If a letter is in a word more than once, reduce value of any other occurences. Magic number seems freq/5. 
                    score += float(self.letter_freq_value[self.letter_freq.index(letter)])/5
                letters.append(letter)
                i += 1
            # Now, we add a value based upon frequency of common letter pairs. 
            for pair in self.letter_pairs:
                if pair in word:
                    score += float(self.letter_pairs_freq[self.letter_pairs.index(pair)])
            self.score_list.append(score)
        # Sort the list of scores.
        zipped_list = sorted(zip(self.score_list, self.word_list), reverse=True)
        self.word_list = [self.word_list for score_list, self.word_list in zipped_list]
        self.score_list = sorted(self.score_list, reverse=True)
        return zipped_list

    # Process input and adjust the word list starting with known letters in the target word
    def process_guess(self, input_list, iteration):
        # Known letter and position [Green square]
        i = 0
        for letter in input_list:
            if letter == "g":
                self.add_known_letters(self.word_history[iteration][i])
                self.letter_place(i, self.word_history[iteration][i], False)
                self.target_word[i] = self.word_history[iteration][i]
            i +=1

        # Known letter but not position [Yellow square]
        i = 0
        for letter in input_list:
            if letter == "y":
                self.add_known_letters(self.word_history[iteration][i])
                self.letter_place(i, self.word_history[iteration][i], True)
                self.letter_modify(self.word_history[iteration][i], False)
            i +=1
        
        # Known not a letter in the target word [Blank square]
        i = 0
        for letter in input_list:
            if letter == "b":
                self.letter_modify(self.word_history[iteration][i], True)
                self.add_known_not_letters(self.word_history[iteration][i])
            i += 1

    # Wordle logic for running tests
    def wordle_logic(self, guess, wordle):
        i = 0
        output = []
        for letter in guess:
            if letter == wordle[i]:
                output.append("g")
            elif letter in wordle:
                output.append("y")
            elif letter not in wordle:
                output.append("b")
            else:
                print("Something bad happened.")
            i += 1
        if len(output) != 5:
            print("Something bad happened x2.")
        return output

# Automatically play Wordle for testing code, start words, etc.
def play_bot(solver, target_list, start_word, verbose):
    succsess = []
    solver.word_list = []
    word_list_sorted = []
    score_list_sorted = []
    fails = 0
    for word in target_list:
        solver.word_list.append(word)

    # Sort by frequency and backup those values
    scores = solver.sort_by_freq()
    for word in solver.word_list:
        word_list_sorted.append(word)
    for score in solver.score_list:
        score_list_sorted.append(score)

    for wordle in target_list:
        if verbose: print("Wordle: %s" % wordle, end='\r')
        solver.word_list = []
        solver.word_history = []
        solver.yellow_green_list = []
        solver.score_list = [] 

        # Copy the saved frequency values instead of calculating them again
        for word in word_list_sorted:
            solver.word_list.append(word)
        for score in score_list_sorted:
            solver.score_list.append(score)

        i = 0
        for i in range(0, 6):
            if i == 0:
                solver.word_history.append(start_word)
                guess = solver.wordle_logic(start_word, wordle)
            else:
                solver.word_history.append(solver.word_list[0])
                guess = solver.wordle_logic(solver.word_list[0], wordle)
            solver.process_guess(guess, i)
            if ''.join(guess) == "ggggg":
                succsess.append(i + 1)
                break
            if len(solver.word_list) == 1:
                succsess.append(i + 1)
                break
            if i == 5:
                fails += 1
            if solver.word_list[0] in solver.word_history:
                solver.word_list.pop(0)
    count = 0
    for i in succsess:
        count += i
    return count, succsess, fails


# Using each word in the word list as a Wordle, try to solve it and see what the average number of guesses is
def test():
    start_word = "least"
    successes = []
    fails = 0
    target_list = []
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    for word in solver.word_list:
        target_list.append(word)
    count, successes, fails = play_bot(solver, target_list, start_word, True)
    print("Number of wordles: %s" % len(target_list))
    print("Number of succsess: %s" % len(successes))
    print("Average guesses for successes: %s" % (count/len(successes)))
    print("Fails: %s" % fails)

# Using each word in the word list as a Wordle, try to solve it and see what the average number of guesses is
def test_start_words():
    averages = []
    target_list = []
    start_word_list =[]
    start_word = "least"
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    for word in solver.word_list:
        start_word_list.append(word)
    for word in solver.word_list:
        target_list.append(word)
    for start_word in start_word_list:
        successes = []
        fails = 0
        count, successes, fails = play_bot(solver, target_list, start_word, False)
        averages.append((count/len(successes), start_word))
        print((count/len(successes), start_word), len(successes))
    result = sorted(averages)
    print("The best start word is %s with a average of %f Wordle guesses." % (result[0][1], result[0][0]))

# Solve a Wordle with a user
def play():
    start_word = "least"
    solver = WordleSolve("5_letter_word_list.txt", start_word)
    solver.stats()
    print("Begin with:")
    scores = solver.sort_by_freq()
    print(solver.box([start_word]))
    solver.word_history.append(start_word)
    i = 0
    for i in range(0, 6):
        user_input = solver.get_input()
        solver.process_guess(user_input[:5], i)
        solver.stats()
        print("Top words:")
        try:
            for x in range(0, 4):
                print("""%s (Freq score: %.2f)""" % (solver.word_list[x], round(solver.score_list[x], 2)))
        except Exception as e:
            pass
        if len(solver.word_list) == 1:
            if ''.join(user_input[:5]) == "ggggg":
                print(solver.box(solver.word_history))
            else:
                print(solver.box(solver.word_history + [solver.word_list[0]]))
            print("Done! Hooray!!")
            exit()
        if solver.word_list[0] in solver.word_history:
            solver.word_list.pop(0)
        print(solver.box(solver.word_history + [solver.word_list[0]]))
        solver.word_history.append(solver.word_list[0])
    print("Oof. Good luck picking final word!")

# Main
if __name__ == "__main__":
    startTime = time()
    if len(argv) == 1:
        print("Try again.")
    elif argv[1] == "test":
        test()
    elif argv[1] == "play":
        play()
    elif argv[1] == "test_start_words":
        test_start_words()
    else:
        print("Try again.")
    executionTime = (time() - startTime)
    print('Time: ' + str(executionTime))

{% endhighlight %}
