from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import roundstatusloc
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p',
    'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
#Reads through our dictionary txt file and creates a word list
    global dictionary
    # Read dictionary file in from dictionary file location
    f = open(dictionaryloc, 'r')
    word_list = f.readlines()
    # Storing each worf read in into a list and ensuring they are lower case
    for i in range(len(word_list)):
        word_list[i] = str(word_list[i]).strip().lower()
        # print(dictionary)
    # Setting dictionary equal to the word list we created
    dictionary = word_list

def readTurnTxtFile():
#Reads in the turn status "message" from txt file
    global turntext   
    #read in turn intial turn status "message" from file
    f = open(turntextloc, 'r')
    turntext = f.read()

def readFinalRoundTxtFile():
#Reads in the final round message from txt file
    global finalroundtext 
    f = open(finalRoundTextLoc, 'r')
    finalroundtext = f.read()  
    #read in turn intial turn status "message" from file

def readRoundStatusTxtFile():
#reads in the round status from the txt file Round Status Txt
    global roundstatus
    f = open(roundstatusloc, 'r')
    roundstatus = f.read() 

def readWheelTxtFile():
#Reads the Wheel text and makes a list of each of the wheel possibilities. 
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    f = open(wheeltextloc, 'r')
    wheellist = f.readlines()
    
def getPlayerInfo():
#Gets the player names and adds that to the variable "players"
    global players
    # read in player names from command prompt input
    # Prompt players to give their names

    print("Please enter player information!")
    #Inputting player names until 3 slots are filled
    Player_Names_In = False
    i = 0
    while (not Player_Names_In):
        #Player Name Inputted
        print(f'Enter your name, Player {i+1}')
        name = input(f'  Player {i + 1}\'s name: ')

        players[i]['name'] = name
        i = i + 1
        if (i == 3):
            print('All Player names have been inputted!\n')
            Player_Names_In = True


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
#This function picks a random word from the dictionary list and creates an underscore version of it
    global dictionary
    #choose random word from dictionary
    i = random.randint(0, len(dictionary))
    roundWord = dictionary[i]
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = ['_' for i in roundWord]
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
#This function sets up the beinning of a round by resetting round totals, picking the first player randomly,
#and getting a random word
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0
    # Return the starting player number (random)
    initPlayer = random.randint(0, 2)
    print(f"{initPlayer + 1}")
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundandBlankWord = getWord()
    roundWord = roundandBlankWord[0]
    blankWord = roundandBlankWord[1]
    return initPlayer


def spinWheel(playerNum):
#Parameters: take in player number. Returns if player is still in turn
#This function "spins" the wheel and resolves what action must be taken for different spin possibilities
#bankruptcy sets round total to 0 and ends turn, lose-a-turn ends turn, and other values will have the player guess a letter
#and ensure that that letter is a consonant. Giving reward if its a correct guess.
    global wheellist
    global players
    global vowels

    # Get random value for wheellist
    i = random.randint(0, len(wheellist) - 1)
    wheelResult = wheellist[i]
    # Check for bankrupcy, and take action.
    if (wheelResult == 'BANKRUPT'):
        #take away players round money. End Turn
        print("Sorry! You landed on BANKRUPTCY! Your round total is now 0!")
        players[playerNum]["roundtotal"] = 0
        stillinTurn = False
    elif (wheelResult == 'Lose_A_Turn'):
        #End Turn
        print("Sorry! You landed on Lose A Turn!")
        stillinTurn = False
    else:
        # Get amount from wheel if not loose turn or bankruptcy
        valid_guess = False
        guess = ''
        # Ask user for letter guess
        while not valid_guess:
            guess = str(input(f'You landed on {wheelResult}, enter in your letter guess: '))
            if (guess in consonants):
                # Use guessletter function to see if guess is in word, and return count
                stillinTurn, count = guessletter(guess)
                valid_guess = True
                # Change player round total if they guess right.     
                if stillinTurn:
                    players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] + int(wheelResult)
            else: print("Sorry! The letter you entered is not a consonant, please enter your guess again: ")
        
    return stillinTurn


def guessletter(letter): 
# parameters:  take in a letter guess. Returns goodGuess = true if the letter was a correct guess, count of times letter appeared
#This function determines if the player guessed a letter in the word and then replaces the underscore to the letter if the letter
#exists there. 
    global blankWord
    global roundWord
    # ensure letter is a consonate.
    count = 0
    if letter in roundWord:
        indexlist = [i for i, ltr in enumerate(roundWord) if ltr == letter]
        for i in indexlist:
            blankWord[i] = letter
            count = count + 1
        # return count of letters in word. 
        print(f'You guessed one of the letters! Here are the letters you have found! {blankWord}. You uncovered {count} of the letters!')
        goodGuess = True
    else: #if the letter was not in the word
        print(f'Sorry, {letter} was not in the word!')
        goodGuess = False
    return goodGuess, count

def buyVowel(playerNum):
#Parameters: take in a player number. Return goodGuess = true if letter appears int he word
#This function is called when a player buys a vowel. If they don't have $250, then they go back to pick a different choice. 
    global players
    global vowels
    vowelGuess = ''
    valid_guess = False
    # Ensure player has 250 for buying a vowelcost
    if (players[playerNum]["roundtotal"] > 250):
        while not valid_guess:
            vowelGuess = input("Enter your vowel guess!: ")
            # Ensure letter is a vowel    
            if (vowelGuess in vowels):
                # Use guessLetter function to see if the letter is in the file
                goodGuess, count = guessletter(vowelGuess)
                players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] - 250
                valid_guess = True
            else:
                vowelGuess = ("Sorry that is not a vowel! Try again! ")
    else:
        print("Sorry! You do not have enough money to guess a vowel!")
        wofTurn(playerNum)    
    return goodGuess      
        
def guessWord(playerNum):
#This function is where players will guess what the word is. It returns "False" for players still being in turn
#If player correctly guesses the word, the blank word is revealed to be the round word
    global players
    global blankWord
    global roundWord

    print(f"This is where the word currently is: {blankWord}")
    wordGuess = str(input("Please input your word guess! "))
    wordGuess = wordGuess.lower()
    playerName = players[playerNum]["name"]
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    if (wordGuess == roundWord):
        blankWord = list(wordGuess)
        print(f"Congratulations {playerName}! You guessed the word!")
    else:
        print(f"Sorry {playerName}, {wordGuess} was not the word!")

    # return False ( to indicate the turn will finish)  
    return False
    
    
def wofTurn(playerNum): 
#Parameters: Takes in the player number
# This is where on their turn a player will choose to spin the wheel, buy a vowel, or guess the word 
    global roundWord
    global blankWord
    global turntext
    global players

    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    stillinTurn = True
    while stillinTurn:
    # output the status for the round
        print(turntext.format(p1_name = players[0]["name"], Round_total_p1 = players[0]["roundtotal"], 
            p2_name = players[1]["name"], Round_total_p2 = players[1]["roundtotal"], 
            p3_name = players[2]["name"], Round_total_p3 = players[2]["roundtotal"],
            p_current = players[playerNum]["name"])) 
        # Get user input S for spin, B for buy a vowel, G for guess the word
        print("You can either spin the wheel, buy a vowel, or guess the word!")
        print(f"The hint is now: {blankWord}")
        correct_option = False
        while not correct_option:
            choice = input(f"What would you like to do player {playerNum + 1}? ")      
            if(choice.strip().upper() == "S"):
                stillinTurn = spinWheel(playerNum)
                correct_option = True
            elif(choice.strip().upper() == "B"):
                stillinTurn = buyVowel(playerNum)
                correct_option = True
            elif(choice.upper() == "G"):
                stillinTurn = guessWord(playerNum)
                correct_option = True
            else:
                print("Not a correct option")        

def wofRound():
#This function rotates through players and uses the wofTurn function to run each player's turn
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
    WordNotFound = True
    while WordNotFound:
        
        if "_" in blankWord:
            # Use the wofTurn fuction to dive into each players turn until their turn is done.
            wofTurn(initPlayer)
            initPlayer = initPlayer + 1
            if initPlayer > 2:
                initPlayer = 0
        else:
            #Winner of round round total sent to their game total
            players[initPlayer]["gametotal"] = players[initPlayer]["gametotal"] + players[initPlayer]["roundtotal"]
            # Print roundstatus tell people the state of the round as you are leaving a round.
            print(roundstatus.format(PlayerName = players[initPlayer]["name"], p1_name = players[0]["name"], Game_total_p1 = players[0]["gametotal"], 
            p2_name = players[1]["name"], Game_total_p2 = players[1]["gametotal"], 
            p3_name = players[2]["name"], Game_total_p3 = players[2]["gametotal"]))
            WordNotFound = False

def wofFinalRound():
#This funtion finds the player with the highest game total and then has them run through the final round. 
#Automatically filling in R, S, T, L, N, E. Letting them pick 3 consonants and 1 vowel. Then allowing one guess for the word
    global players
    global roundWord
    global blankWord
    global finalroundtext
    global consonants
    global vowels
    winplayer = 0
    
    #get list of game totals to find the player with the highest amount
    gametotals = []
    for i in range(0, len(players) - 1):
        gametotals.append(players[i]["gametotal"])
    winplayer = gametotals.index(max(gametotals))
    winner = players[winplayer]["name"]
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(PlayerName = winner))
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    roundandBlankWord = getWord()
    roundWord = roundandBlankWord[0]
    blankWord = roundandBlankWord[1]
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    startingLetters = ['r', 's', 't', 'l', 'n', 'e']
    i = 0
    for i in range(0,len(startingLetters)):
        letter = startingLetters[i]
        guessletter(letter)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f"After the beginning letters have been put in the word is now: {blankWord}")
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    correctInput = False
    #This loop ensures that players are putting in the correct input of 3 consonants and 1 vowel
    while not correctInput:
        userLetters = [str(x) for x in input("Enter three consonants and one vowel separated by a space: ").split()]
        consonantCount = 0
        vowelCount = 0 
        if len(userLetters) != 4:
            correctInput = False
        else:
            for i in range(0,len(userLetters)):
                if userLetters[i] in consonants:
                    consonantCount = consonantCount + 1
                    if consonantCount > 3:
                        correctInput = False
                elif userLetters[i] in vowels:
                    vowelCount = vowelCount + 1
                    if vowelCount > 1:
                        correctInput = False
                else:
                    correctInput = False
        if consonantCount == 3 and vowelCount == 1:
            correctInput = True
    #Running each letter guess through the function
    i = 0
    for i in range(0,len(userLetters)):
        letter = userLetters[i]
        guessletter(letter)
    # Print out the current blankWord again
    print(f"With your guesses in the word now looks like: {blankWord}")
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    print("You will now get one chance to guess the word! Good luck!")
    lastGuess = str(input("Put in your guess! "))
    lastGuess = lastGuess.lower()
    # Take user input of the word and check if it is the same as roundWord
    if (lastGuess == roundWord):
        blankWord = list(lastGuess)
        print("Congratulations! you guessed the word!")
        players[winplayer]["gametotal"] = players[winplayer]["gametotal"] + 25000
    else:
        print(f"Sorry {lastGuess} was not the word!")
    # If they do, add finalprize and gametotal and print out that the player won 
    finalTotal = players[winplayer]["gametotal"]
    print(f"We have finished the game! {winner} did a great job and is going home with ${finalTotal}!")

def main():
#This function is the main function that runs through the others and ensures there are 3 rounds (2 regular 1 final)
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            print(f"Let's begin round {i+1}!")
            wofRound()
        else:
            print("It's time to begin the final round!")
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
