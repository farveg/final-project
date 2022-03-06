import re
import nltk
from nltk.corpus import inaugural, switchboard
nltk.download('punkt')

# A for-loop which iterates over the files in the Inaugural Corpus and reates a list of tuples, each containing the name of the file at [0] and its contents at [1].

speeches = []

for file in inaugural.fileids():
	x = inaugural.raw(file)
	y = (file, x)
	speeches.append(y)

proper_noun = re.compile(r'[A-Z]\w+\b')
number = re.compile(r'[0-9]\w+\b')

# A for-loop which iterates over the tuples in 'speeches' to compute the TTR for each inaugural address, then prints this information out.

for pair in speeches:
	tokens = nltk.word_tokenize(pair[1])
	ttr = len(tokens) / len(pair[1])
	name = re.search(proper_noun, pair[0])[0]
	date = re.search(number, pair[0])[0]
	print(f"{name}'s {date} Inaugural Address has a TTR of {ttr}")

# Some regex pattens to filter out the following content from the SwitchBoard transcript:
	# Speaker and utterance number
	# <Laughter> and other situational descriptors
	# Loose symbols (-, --, and +)

# note: Decide how to deal with disfluencies e.g. "uh-", "we- well"

speakers = re.compile(r'(A|B)\.[0-9]+:\s')
descriptions = re.compile(r'\s<\w+\b>(\s|\.|\?|,)')
misc = re.compile(r'\s(-|--|\+)\s')
punctuation = re.compile(r'\.|,|\?')

switchboardRaw = switchboard.raw('transcript')

switchBoard = re.sub(speakers,'', switchboardRaw)
switchBoard = re.sub(descriptions,'', switchBoard)
switchBoard = re.sub(misc,' ', switchBoard)
switchBoard = re.sub(punctuation,'', switchBoard)

# Creates a list by splitting 'switchboardRaw' at the double newLine break, which separates the string into a list 'convos' containing 36 conversations. A for-loop is passed over that list 'convos' to filter out the same content as previously and then add each filtered conversation to a new list 'conversations'.

conversations = []
convos = switchboardRaw.split('\n\n')

for convo in convos:
	x = re.sub(speakers, '', convo)
	x = re.sub(descriptions, '', x)
	x = re.sub(misc, ' ', x)
	x = re.sub(punctuation, '', x)
	conversations.append(x)

# A for-loop which iterates over 'conversations' to compute the TTR for each conversation, then prints this information out.

counter = 0
for conversation in conversations:
	tokens = nltk.word_tokenize(conversation)
	ttr = len(tokens) / len(conversation)
	counter += 1
	print(f'Conversation {counter} has a TTR or {ttr}')

# TF-IDF scores

# The idea is to write a function or set of functions which can compute the TF-IDF score of all the words in each conversation in 'conversations', and then rank-order the results to display the most/least relevant words in each document.

# To do this will require a program which can loop over the values in each element of 'conversations', compute the TF and the IDF scores for each value, multiply these scores together to give the TF-IDF score for each value, and then add that score as a value to a dictionary whose key is the word it corresponds to. There should be 36 dictionaries total, one for each conversation, which can be sorted based on values to display the most and least relevant words in each document.

import math

# For now I've managed to write a function which takes a string as input and prints out the IDF score for that string. I'll need to store that value so that I can further manipulate it, and figure out how to loop over each of the words in each 'conversation' rather than just a manually declared input.

def getIDF(word):
	counter = 0
	for conversation in conversations:
		if re.search(word, conversation):
			counter+=1
	if counter > 0:		
		idf = math.log(len(conversations) / counter)
	else:
		idf = 0	
	print(idf)
	
getIDF('understandable')

instructions = """
	Term Frequency - Inverse Document Frequency
	TF-IDF = xy, where

	x = The term frequency of a word in a document. There are several ways of calculating this frequency, with the simplest being a raw count of instances a word appears in a document. Then, there are ways to adjust the frequency, by length of a document, or by the raw frequency of the most frequent word in a document.

	y = The inverse document frequency of the word across a set of documents. This means, how common or rare a word is in the entire document set. The closer it is to 0, the more common a word is. This metric can be calculated by taking the total number of documents, dividing it by the number of documents that contain a word, and calculating the logarithm.

= log ( N / count(d in D :t in d)), where 
t is a word, d a document, D a document set, and N len(D)
"""

print(instructions)
