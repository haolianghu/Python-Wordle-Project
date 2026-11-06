# Date: 04-30-2022
# Description of Program: this program implement a version of Wordle. 
# The answer will be a 5-letter word that is selected randomly from a wordlist (if not specified). 

import os.path
import random
from wordle_common import create_wordlist, feedback

def createWordlist(filename): 
    """Load playable words from a file."""
    return create_wordlist(filename)

def BinarySearch ( lst , key ):
    """ Search for key in sorted list lst. """ 
    low = 0 
    high = len ( lst ) - 1 
    
    while ( high >= low ):
        mid = ( low + high ) // 2 
        if key < lst [mid]:
            high = mid - 1 
        elif key == lst [ mid ]:
            return mid
        else :
            low = mid + 1

def playWordle(answer = None):
    #Display instructions for how to play Wordle
    print("Welcome to WORDLE, the popular word game. The goal is to guess a \
         \nfive letter word chosen at random from our wordlist. None of the \
         \nwords on the wordlist have any duplicate letters.")
    print()
    print("You will be allowed 6 guesses. Guesses must be from the allowed \nwordlist. We'll tell you if they're not.")
    print()
    print("Each letter in your guess will be marked as follows:")
    print()
    print("   x means that the letter does not appear in the answer \
         \n   ^ means that the letter is correct and in the correct location \
         \n   + means that the letter is correct, but in the wrong location")
    print()
    print("Good luck!")
    print()

    #Have the user enter the name of the word list file
    filename = input("Enter the name of the file from which to extract the wordlist: ")
    #Exception handling
    while os.path.isfile(filename) != True:
        print("File does not exist. Try again!")
        filename = input("Enter the name of the file from which to extract the wordlist: ")
    wordlist = createWordlist(filename)
    if not wordlist:
        print("The file contains no playable words.")
        return

    #Set the answer word to be random if not specified
    answerLegal = True
    if answer != None:
        if BinarySearch(wordlist, answer) == None:
            print("Answer supplied is not legal.")
            answerLegal = False
    else:
        answer = random.choice(wordlist)

    #Have the players input guesses
    print()
    attempts = 1
    win = False
    while answerLegal == True and attempts <= 6 and win == False:
        guess = input("Enter your guess " + "(" + str(attempts) + "): ")
        guess = guess.lower()
        while len(guess) != 5 or BinarySearch(wordlist, guess) == None:
            print("Guess must be a 5-letter word in the wordlist. Try again!")
            guess = input("Enter your guess " + "(" + str(attempts) + "): ")
            guess = guess.lower()

        #Show the players the characters they got correct and wrong
        result = feedback(answer, guess)
        print("  ".join(guess.upper()))
        print("  ".join(result))

        #Check if the player has all characters guessed correctly and print results
        if result == "^^^^^":
            print ("CONGRATULATIONS! You win!")
            win = True
    
        attempts += 1

    #If all the attempts are used, terminate the game
    if answerLegal == True and win == False:
        print("Sorry! The word was", answer + '.', "Better luck next time!")
        print()

if __name__ == "__main__":
    playWordle()
