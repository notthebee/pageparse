#! /bin/python3

from bs4 import BeautifulSoup
from sw import stopwordList
import urllib.request
import nltk
import enchant
from matplotlib import pyplot as plt
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
ap.add_argument("url", 
                help="URL of the page, for example: https://en.wikipedia.org/)" or "fsf.org")
ap.add_argument("-l", "--lang", 
                required=False, 
                default="english", 
                help="Language of the webpage (english, french, russian, spanish, german, italian, portuguese). Requires optional dependencies to be installed. Defaults to English")
ap.add_argument("-w", "--wordnum",
				required=False,
				type=int,
				default=20,
				help="Number of words in the graph. Defaults to 20")
ap.add_argument("-n", "--nospellcheck",
                required=False,
                action='store_true',
                help="Turn off spellchecking")
ap.add_argument("-e", "--exclude", 
                required=False, 
                help='Exclude words from the graph, divided by spaces. For example: "lorem ipsum dolor sit amet"')
args=vars(ap.parse_args())

# Appending http:// to the URL in case not specified by the user
url = args["url"]
if not url.startswith("http"):
	url = "http://" + url

# Checking if the language is valid
lang = args["lang"]
valid_languages=("english", "french", "russian", "spanish", "german", "italian", "portuguese")
if not args["lang"] in valid_languages:
    print("ERROR: Invalid language. Supported options: english, french, russian, spanish, german, italian, portuguese")
    sys.exit(1)

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
words = [word.lower() for word in clean_tokens if word.isalpha()]
sr=stopwordList(stoplang=lang)
clean_words = []
for word in words:
    if not word in sr:
        clean_words.append(word)

# Removing "non-words" and spellchecking unless turned off by user
def spellCheck():
    if lang in ['english', 'french', 'italian', 'russian']:
     langshort = lang[:2]
    elif lang == 'german':
        langshort = 'de'
    elif lang == 'spanish':
        langshort = 'es'
    elif lang == 'portuguese':
        langshort == 'pt'
    d = enchant.Dict(langshort)
    correct_words = []
    for word in clean_words:
        if d.check(word):
            correct_words.append(word)
    return correct_words
if args["nospellcheck"] == False:
    correct_words = spellCheck()
else:
    correct_words = clean_words
# Also excluding the words if specified by the user
if args["exclude"]:
	exclude = args["exclude"].split()
	words = [word for word in correct_words if word not in exclude]
else:
    words = [word for word in correct_words]

# Displaying the plot
freq = nltk.FreqDist(words).copy()
freq.plot(args["wordnum"], 
          cumulative=False, 
          title='Frequency plot for ' + url, 
          linewidth=2,
          color='red')
