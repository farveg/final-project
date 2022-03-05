import re
import nltk
from nltk.corpus import inaugural, switchboard
nltk.download('punkt')

# help(nltk.corpus.reader)

switchboardRaw = switchboard.raw('transcript')

speeches = []

for file in inaugural.fileids():
	x = inaugural.raw(file)
	y = (file,x)
	speeches.append(y)

### Content to filter from switchBoard

# Speaker and utterance number
#	- "(A/B).(0-1000):"
# <Laughter> and other situational descriptors
# Decide how to deal with disfluencies e.g. "uh-", "we- well"

speakers = re.compile(r'(A|B)\.[0-9]+:\s')
descriptions = re.compile(r'\s<\w+\b>(\s|\.|\?|,)')
misc = re.compile(r'\s(-|--|\+)\s')
punctuation = re.compile(r'\.|,|\?')

switchBoard = re.sub(speakers,'', switchboardRaw)
switchBoard = re.sub(descriptions,'', switchBoard)
switchBoard = re.sub(misc,' ', switchBoard)
switchBoard = re.sub(punctuation,'', switchBoard)

switchBoard = switchBoard.lower()
switchTokens = nltk.word_tokenize(switchBoard)

ttr = len(switchTokens) / len(switchboard.words())

proper_noun = re.compile(r'[A-Z]\w+\b')
number = re.compile(r'[0-9]\w+\b')

for pair in speeches:
	tokens = nltk.word_tokenize(pair[1])
	ttr = len(tokens) / len(pair[1])
	name = re.search(proper_noun, pair[0])[0]
	date = re.search(number, pair[0])[0]
	print(f"{name}'s {date} Inaugural Address has a TTR of {ttr}")

convos = [x for x in switchboardRaw]
convos = ''.join(convos)	
convos = convos.split('\n\n')

conversations = []

for convo in convos:
	x = re.sub(speakers, '', convo)
	x = re.sub(descriptions, '', x)
	x = re.sub(misc, ' ', x)
	x = re.sub(punctuation, '', x)
	conversations.append(x)

counter = 0

word = re.compile(r'\w+\b')

for conversation in conversations:
	tokens = nltk.word_tokenize(conversation)
	ttr = len(tokens) / len(conversation)
	counter += 1
	print(f'Conversation {counter} has a TTR or {ttr}')
