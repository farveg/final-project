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

switchTokens = nltk.word_tokenize(switchBoard.lower())

# How neecessary is any of this section? 'ttr' gives TTR of whole corpus, not desired.

ttr = len(switchTokens) / len(switchboard.words())

print(ttr)

# Creates a list by splitting 'switchboardRaw' at the double newLine break, which separates the string into a list 'convos' containing 36 conversations. A for-loop is passed over that list 'convos' to filter out the same content as previosly and then add each filtered conversation to a new list 'conversations'.

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


