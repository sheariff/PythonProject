# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:28:26 2018

@author: User
"""
import numpy as np
import re
import matplotlib.pyplot as plt

plt.rcdefaults()


# Reads in data, splits up each word and makes lowercase
def readFile(src):
    text_file = open(src)
    read_file = text_file.read()  # Variable holding the full unedited tweets
    word_list = read_file.lower().split()  # Splits up each word seperately into all lowercase
    return word_list


# Filters out the keys that aren't allowed
def formatW(word_list):
    # sets the allowed keys
    Words = re.compile("[^A-Za-z0-9]+")

    # filters through your word list keeping only the allowed words
    return list(filter(lambda cursedWord: not Words.search(cursedWord), word_list))


# Counts the times each word appears, sets it as the value for the dictionary passed in
def occuringwords(clean_list, dictionary):
    for word in clean_list:  # For each word in clean_list
        dictionary[word] += 1  # Increments key by one

    return dictionary


# Works out from the full dictionary the probability any given word is positive
def trainwordspos(posDictionary, fullDictionary):
    vocabPositive = {}  # Dictionary that stores the probability that a word is positive as its value
    for word in fullDictionary:
        fOccurance = fullDictionary[word]
        posProbability = (posDictionary[word] / fOccurance)

        vocabPositive[word] = posProbability

   
    return vocabPositive


def predictions22(testTweets, fullDictionary, vocabPositive, vocabNegative, positiveOrNegativeFile):
    Verdict = {}  # Dictionary that stores if the algorithm thinks the tweet is positive or negative
    # Initialise varibles used to count how many are predicted positive or negative
    postweet, negtweet = 0, 0

    # Loops through words in the tweet to find any trained to be positive/negative
    for tweet in testTweets:
        tweetWords = re.split(r"[^\w]", tweet)  # Should clean up the special characters.
        positiveCount = 1
        negativeCount = 1  # Initialise varibles needed foe the loop

        # Loops through each word in the tweet, if it appeared in the trainer it goes through and grabs the probability. Then adds that to the total probability and ups counted words
        for word in tweetWords:
            # if vocabPos.__contains__(word):
            if word in vocabPositive.keys():
                if fullDictionary[word] > 1:  # Ignores any word that appears onceb
                    positiveCount *= vocabPositive[word]
                    negativeCount *= vocabNegative[word]

        if positiveCount > negativeCount:
            Verdict[tweet] = "Positive"
            postweet += 1

        elif positiveCount == negativeCount:
            Verdict[tweet] = "Undecided"

        else:
            Verdict[tweet] = "Negative"
            negtweet += 1

    print("Positive Tweets  ", postweet, "Negative tweets:", negtweet)
    # -----------------------------------------------
    # Getting Accuracy
    # -----------------------------------------------
    # Counts length of the Count
    # count = len(testTweets)

    # Works out the accuracy
    accuracyPos = ((postweet / (postweet + negtweet)) * 100)
    accuracyNeg = ((negtweet / (postweet + negtweet)) * 100)

    if positiveOrNegativeFile == True:
        print(f"The positive accuracy is {accuracyPos}")
        return accuracyPos
    else:
        print(f"The negative accuracy is {accuracyNeg}")
        return accuracyNeg


# It reads in the test data we were given, finds each word from our dictionary and works out from that how likey a tweet is to be positive or negative
def Perdictions1(positiveDictionary, negDictionary, Dictionary, vocabPositive):
    # -------------------------------------------
    # Assigning the likelyhood of a word being Positive/Negative
    # -------------------------------------------
    Verdict = {}  # Dictionary that stores if the algorithm thinks the tweet is positive or negative

    # Opens in file seperated by tweets
    tweetsPositive = open("testPos.txt", 'r').read().lower().split("\n")
    # Combines full list of tweets
    # tweets = tweetsPos + tweetsNeg

    # Initialise varibles used to count how many are predicted positive or negative
    postiveTweets, negativeTweets = 0, 0

    # Loops through words in the tweet to find any trained to be positive/negative
    for tweet in tweetsPositive:
        tweetWords = re.split(r"[^\w]",
                              tweet)  # Should clean up the special characters. TODO: Test this is properly fundtioning
        probOfPos, count, posCount, negCount = 1, 0, 1, 1  # Initialise varibles needed foe the loop

        # Loops through each word in the tweet, if it appeared in the trainer it goes through and grabs the probability. Then adds that to the total probability and ups counted words
        for word in tweetWords:
            if vocabPositive.__contains__(word):
                count += 1  # counts words considered

                if vocabPositive[word] > 0.5:
                    posCount *= vocabPositive[word]
                elif vocabPositive[word] == 0.5:
                    next1 = 0
                else:
                    negCount *= vocabPositive[word]

        if posCount > negCount:
            Verdict[tweet] = "Positive"
            postiveTweets += 1
        elif posCount == negCount:
            Verdict[tweet] = "Undecided"
        else:
            Verdict[tweet] = "Negative"
            negativeTweets += 1

    print("Positive Tweets Identified: ", postiveTweets, "Negative:", negativeTweets)

    # -----------------------------------------------
    # Getting Accuracy
    # -----------------------------------------------
    # Counts length of the Count
    positiveCounter = len(tweetsPositive)
    # negativeCount = len(tweetsNeg)
    # Works out the accuracy
    accuracyPos = ((postiveTweets / positiveCounter) * 100)
    accuracyNeg = ((negativeTweets / positiveCounter) * 100)
    print(f"The positive accuracy is {accuracyPos} \nThe negative accuracy is {accuracyNeg}")

    # -------------------------------------
    # DATA VISUALIZATION
    # ------------------------------------
    # plots the graph
    y_position = [-1, round(accuracyNeg)]
    object = ('Processed +ve Accuracy', 'Processed -ve Accuracy')
    plot = [accuracyPos, accuracyNeg]
    y_posi = np.arange(len(object))
    plt.bar(y_position, plot, align='center', alpha=0.1)
    plt.xticks(y_posi, object)
    plt.ylabel("Value")
    plt.xlabel("Data")
    plt.title("Visualization")
    plt.show()


# Reads in the File and sorts it into the dictionary.
def main():
    # -------------------------------------------
    # READING IN DATA & SETTING UP DICTIONARY :
    # -------------------------------------------
    # Opens text file in read only
    posList = readFile("trainPos.txt")
    negList = readFile("trainNeg.txt")

    # Gets rid of special characters
    cleanPosList = formatW(negList)
    cleanNegList = formatW(posList)

    # Creates a set of just unique words from the list of words
    uniquePos = set(cleanPosList)
    uniqueNeg = set(cleanNegList)

    # Makes a full list of words from Positive and Negative
    fullSet = uniquePos | uniqueNeg

    # Creates a dictionary setting the value of each fullList to 0 for counting
    posDictionary = dict.fromkeys(fullSet, 0)
    negDictionary = dict.fromkeys(fullSet, 0)
    fullDictionary = dict.fromkeys(fullSet, 0)

    # --------------------------------------------------------
    # GETTING OCCURANCE OF EACH WORD
    # --------------------------------------------------------
    posDictionary = occuringwords(cleanPosList, posDictionary)
    negDictionary = occuringwords(cleanNegList, negDictionary)
    # Combined wordcount
    for word in cleanPosList:  # For each word in clean_list
        fullDictionary[word] += 1
    for word in cleanNegList:  # Then also adds in clean_list2
        fullDictionary[word] += 1


    # ----------------------------------------------------------------------------------------------------
    # GETTING PROBABILITY OF A WORD BEING POSITIVE / NEGATIVE
    # ----------------------------------------------------------------------------------------------------
    vocabPos = trainwordspos(posDictionary, fullDictionary)
    vocabNeg = trainwordspos(negDictionary, fullDictionary)
    # print(vocabNeg)
    # -----------------------------------------------------------------------------------
    # PREDICT IF TWEETS ARE POSITIVE OR NEGATIVE & Data Visualization
    # -----------------------------------------------------------------------------------

    # Opens in file seperated by tweets
    tweetsPos = open("testPos.txt", 'r').read().lower().split("\n")
    tweetsNeg = open("testNeg.txt", 'r').read().lower().split("\n")

    posAccuracy = predictions22(tweetsPos, fullDictionary, vocabPos, vocabNeg, True)
    negAccuracy = predictions22(tweetsNeg, fullDictionary, vocabPos, vocabNeg, False)
    totalAccuracy = (posAccuracy + negAccuracy / 2)
    print(f"The total Accuracy is {totalAccuracy}")
    # -------------------------------------
    # DATA VISUALIZATION
    # ------------------------------------
    # plots the graph
    y_position = [-1, round(negAccuracy)]
    objects = ('Processed +ve Accuracy', 'Processed -ve Accuracy')
    plotlocation = [posAccuracy, negAccuracy]
    y_posi= np.arange(len(objects))
    plt.bar(y_position, plotlocation, align='center', alpha=0.1)
    plt.xticks(y_posi, objects)
    plt.ylabel("Value")
    plt.xlabel("Data")
    plt.title("Data Visualization")
    plt.show()


main()


