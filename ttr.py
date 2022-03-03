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
print(len(switchTokens))
print(len(switchboard.words()))
print(ttr)


#for speech in speeches:
#	tokens = nltk.word_tokenize(speech)
#	ttr = len(tokens) / len(speech)
#	print(f'This has a TTR of {ttr}.')

for pair in speeches:
	tokens = nltk.word_tokenize(pair[1])
	ttr = len(tokens) / len(pair[1])
	name = pair[0]
	print(f'{name} has a TTR of {ttr}')





