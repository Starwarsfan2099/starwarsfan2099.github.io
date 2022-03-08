---
title: Solving Wordle using Python and Basic Frequency Analysis
excerpt: A quick writeup on a simple way I approached solving Wordle with Python and letter frequency analysis. 
tags: programming fun
author: rms
---

## What's Wordle?

{:refdef: style="text-align: center;"}
![Wordle](../public/2022-03-05/wordle.jpg){:.shadow}
{: refdef}

Wordle is a small online game that has blown up in popularity recently. It's premise is simple, you have six tries to guess a five letter word. I'm going to call this the target word. Each guess reveals information about the target word. If a letter you guessed is at the same place in the target word, it's square in the grid is colored green. If the letter is in the target word but it in the incorrect place, the square is colored yellow. And finally, if the letter is not in the target word the square is blank with no color. 

In the example image above, the first word I guessed was *beach*. "B" is colored green, so the target word starts with a "B". "E" is colored yellow, so the letter "E" is in the word, but is not the second letter in the word. "A", "C", and "H" are not found anywhere in the target word. The next word I guess is *brief*. "B" is the first letter and the letter "E" is in the word and not in the second place. I got lucky and go too more letters that are in the correct space: "R" and "I". The "E" is yellow, so the only other place it can be is the last place. Now we only have to guess one more letter. And from the other guesses we know that "B", "E", "A", "C", "H", and "F" are not letters that can be in the next to last place. My final guess was the word *brine*. All the squares are green, and that was in fact the target word. 

## Frequency analysis?

Frequency analysis is used to determine the frequency of individual letters in the English language. This is shows us what letters are used more frequently than others, for example, the letter "A" is more common in words than "Z". This can be used for solving a Wordle by guessing the most likely word with the information returned from previous guesses. Thankfully, a frequency analysis of all English letters already exists.

{:refdef: style="text-align: center;"}
![Table](../public/2022-03-05/table.jpg){:.shadow}
{: refdef}

Using this information, we can generate a 'score' for each five letter word that is a possible guess or possible Wordle. This score can than be used to determine the *most likely* guess with the given information. Simple really.

## The code.

If you want to see the full source code, it's at the bottom of the post or can be found [here](https://gist.github.com/Starwarsfan2099/600899c8ebbe75e5b3e0bf581c38c5fa). Now, lets walk through the code.

{% highlight python linenos %}
from sys import argv
from time import time

# Wordle Solver class
class WordleSolve:

    def __init__(self, file_name, start_word):

        # Alphabet letters sorted by frequency
        self.letter_freq = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c", "u", "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]
        self.letter_freq_value = ["12.02", "9.10", "8.12", "7.68", "7.31", "6.95", "6.28", "6.02", "5.92", "4.32", "3.98", "2.88", "2.71", "2.61", "2.30", "2.11", "2.09", "2.03", "1.82", "1.49", "1.11", "0.69", "0.17", "0.11", "0.10", "0.07"]
        self.target_word = ["_", "_", "_", "_", "_"]
        self.yellow_green_list = []
        self.not_list = []
        self.word_history = []
        self.score_list = []
        self.start_word = start_word

        # Open a list of 5 letter words and save to memory
        word_list_file = open(file_name, "r")
        self.word_list = word_list_file.read().split()
        word_list_file.close()
        self.word_list_total = len(self.word_list)
{% endhighlight %}

First, `argv` is imported for command line arguments and `time` is imported to time the script later on. Next, a class `WordleSolve` is created and inside it is the constructor function `__init__`. In the constructor, several variables are created and initialized. Firstly, two variables for to help with letter frequency analysis: `letter_freq` and `letter_freq_value`. 