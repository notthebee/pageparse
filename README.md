## pageparse.py

A small script that scrapes a webpage and displays a graph of the most used words  

### optional arguments:  
* -h, --help  
show this help message and exit  
* -l LANG, --lang LANG  
Language of the webpage (english, french, russian, spanish, german, italian, portuguese). Requires optional dependencies to be installed. Defaults to English  
* -e EXCLUDE, --exclude EXCLUDE  
Exclude words from the graph, divided by spaces. For example: "lorem ipsum dolor sit amet"  

### required arguments:
* -u URL, --url URL  
URL of the page, for example: https://en.wikipedia.org/wiki/Python_(programming_language)  

### dependencies:
* BeautifulSoup
* urllib
* nltk
* enchant
* re
* aspell-en

### optional dependencies:
* aspell-fr
* aspell-de
* aspell-es
* aspell-it
* aspell-ru
* aspell-pt
