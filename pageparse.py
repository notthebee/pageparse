#! /bin/python3

from bs4 import BeautifulSoup
import urllib.request
import nltk
import enchant
from nltk.corpus import stopwords
import argparse
import re
import sys

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Arguments
ap = argparse.ArgumentParser(description=color.GREEN + 'A small script that scrapes a webpage and displays a graph of the most used words' + color.END)
requiredNamed = ap.add_argument_group('required arguments')
requiredNamed.add_argument("-u", "--url", required=True, help="URL of the page, for example: https://en.wikipedia.org/wiki/Python_(programming_language)")
ap.add_argument("-l", "--lang", required=False, default="english", help="Language of the webpage (english, french, russian, spanish, german, italian, portugese). Requires optional dependencies to be installed. Defaults to English")
ap.add_argument("-e", "--exclude", required=False, help='Exclude words from the graph, divided by spaces. For example: "lorem ipsum dolor sit amet"')
args=vars(ap.parse_args())

# Checking if the URL is valid
if not args["url"].startswith("http"):
    print("ERROR: Invalid URL (don't forget 'http://' or 'https://')")
    sys.exit(1)
else: url = args["url"]

# Checking if the language is valid
valid_languages=("english", "french", "russian", "spanish", "german", "italian", "portugese")
if not args["lang"] in valid_languages:
    print("ERROR: Invalid language. Supported options: english, french, russian, spanish, german, italian, portugese")
    sys.exit(1)
else: lang = args["lang"]

# Scraping the page
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
response = urllib.request.urlopen( req )
html = response.read()
soup = BeautifulSoup(html, "html5lib")

# Removing all the junk
for script in soup(["script", "style"]):
    script.decompose()
text = soup.get_text(strip = True)
tokens = [t for t in text.split()]
clean_tokens = tokens[:]

# Removing stop words (the, a, an, etc.) and non-alphabetic characters
sr = stopwords.words(lang)
for token in tokens:
    if token in sr:
        clean_tokens.remove(token)
words = [word.lower() for word in clean_tokens if word.isalpha()]

# Removing "non-words"
if lang == 'english' or 'french' or 'italian' or 'russian':
    langshort = lang[:2]
elif lang == 'german':
    langshort = 'de'
elif lang == 'spanish':
    langshort = 'es'
elif lang == 'portugese':
    langshort == 'pt'
d = enchant.Dict(langshort)
correct_words = []
for word in words:
	if d.check(word):
		correct_words.append(word)
# Also excluding the words if specified by the user
if args["exclude"]:
	exclude = args["exclude"].split()
	words = [word for word in correct_words if word not in exclude]
else:
    words = [word for word in correct_words]


freq = nltk.FreqDist(words)
for key,val in freq.items():
    print (str(key) + ':' + str(val))
freq.plot(20, cumulative = False)

