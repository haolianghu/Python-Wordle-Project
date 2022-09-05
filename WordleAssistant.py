# Date: 04/15/2022
# Description of Program: 
# This program provides hints for Wordle. The user can input information and 
# the program will provide some possible solutions to the Wordle the user is solving. 

import os.path

def createWordlist(filename): 
    """" 
    This function:
    Reads words from the word list and store them in a list.
    The file contains only lowercase ascii characters, are sorted alphabetically, one word per line. 
    Filters out any words that are not 5 letters long, have duplicate letters, or end in 's'.  
    Returns the list of words and the number of words as a pair. 
    """

    allWords = open(filename, 'r')
    line = allWords.readline()
    list1 = []
    count = 0

    #Read all the words from the other file
    while line:
        line.strip()
        list1.append(line)
        line = allWords.readline()
    
    #Remove \n from each of the item in the list
    list2 = [word[:-1] for word in list1]
    wordlist =[]

    #Filter out the words
    for word in list2:
        #Check if is 5 letters
        if len(word) == 5:
            #Check if end with s
            if word.endswith('s') == False:
                #Check if there are any repeating letters
                if len(word) == len(set(word)):
                    wordlist.append(word)
                    count += 1
    
    allWords.close()
    return wordlist

def containsAll(wordlist, include):
    """ Given wordlist, return a set of all words from the wordlist
    that contain all of the letters in the string include.  
    """

    setinclude = set()
    for word in wordlist:
        sameCount = 0
        for letter in word:
            for item in set(include):
                if letter == item:
                    sameCount += 1
        if sameCount == len(include):
            setinclude.add(word)
         
    return setinclude

def containsNone(wordlist, exclude):
    """ Given wordlist, return a set of all words from the wordlist
    that do not contain any of the letters in the string exclude.  
    """

    setexlude = set(wordlist)
    for word in wordlist:
        matchCount = 0
        for letter in word:
            if letter in set(exclude):
                matchCount += 1
        if matchCount >= 1:
            setexlude.remove(word)
    
    return setexlude

def containsAtPositions(wordlist, posInfo):
    """ posInfo is a dictionary that maps letters to positions.
    Positions are in [0..4].  Return a set of all words from the 
    wordlist that contain the letters from the dictionary at the 
    indicated positions. 
    For example, given posInfo {'a': 0, 'y': 4}.   
    This function might return the set:
    {'angry', 'aptly', 'amply', 'amity', 'artsy', 'agony'}. """

    wordset = set()
    for word in wordlist:
        dic = {}
        index = 0
        matchCount = 0
        #Creates a dictionary for each letter in the word
        for letter in word:
            dic[letter] = index
            index += 1
        #Check how many matching keys and dictionaries are there
        for key1 in posInfo:
            for key2 in dic:
                if key1 == key2:
                    if posInfo.get(key1) == dic.get(key2):
                        matchCount += 1
        #If amount of matching key and value is equal to input, then add word
        if matchCount == len(posInfo):
            wordset.add(word)

    return wordset

def getPossibleWords(wordlist, posInfo, include, exclude):
    """ After providing wordlist, dictionary posInfo, and
    strings include and exclude, return the set of all words from 
    the wordlist that contains the words that satisfy all of 
    the following:
    * has letters in positions indicated in posInfo
    * contains all letters from string include
    * contains none of the letters from string exclude.
    """

    solution = set()
    for word in containsAtPositions( wordlist, posInfo):
        if word in containsAll( wordlist, include) and word in containsNone( wordlist, exclude):
            solution.add(word)

    return solution
    
#For testing:
#wordlist= createWordlist( 'Wordlist.txt' )
#print(getPossibleWords(wordlist, {'a':0, 'b':1}, "o", "v" ))

def main():
    '''
    Prompts the user to input known information
    '''
    
    #Input file name of the word list
    filename = input("Enter the name of the file from which to extract the wordlist: ")
    #Exception handling
    while os.path.isfile(filename) != True:
        print("File does not exist. Try again!")
        filename = input("Enter the name of the file from which to extract the wordlist: ")
    wordlist = createWordlist(filename)

    #Input known correct characters and their positions:
    number_of_characters = int(input("Enter the number of correctly guessed characters with known positions: "))
    dictionary = {}
    for i in range(1, number_of_characters+1):
        print("Please enter the #" , i, " character: ", sep = '')
        character = input()
        print("Please enter the position of the #", i, " character, with the first position starting at 0", sep='')
        position = int(input())
        dictionary[character] = position

    #Input characters to inlcude and exclude
    characters_include = input("Enter the characters to include (e.g. abc): ")
    characters_exclude = input("Enter the characters to exclude (e.g. abc): ")

    #Call the previous function to find the potential solutions
    print(getPossibleWords(wordlist, dictionary, characters_include, characters_exclude))

main()
