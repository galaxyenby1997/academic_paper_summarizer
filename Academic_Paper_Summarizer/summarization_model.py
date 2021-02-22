# --------------------- Import Gensim software and Beautifulsoup --------------
from gensim.summarization import summarize, keywords
import requests
from bs4 import BeautifulSoup as soup
import re

# -------------------- Import NLTK Libraries ------------------------
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
# --------------------------------------------------
wnl = WordNetLemmatizer()
# helper function below
# This will covert Treebank Tags to Wordnet POS Tags

from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag.startswith('P'):
        return wordnet.NOUN
    else:
        return 'n'

def lemmatize_wordlist(L):
    lemmatized_words = []
    for pair in pos_tag(L):
        wn_tag = get_wordnet_pos(pair[1])
        if wn_tag is not '':
            lemmed_word = wnl.lemmatize(pair[0], wn_tag)
            lemmatized_words.append(lemmed_word)
    return list(set(lemmatized_words))

# Let's extract the list of common spoken english words from saved file
common_words = []
with open('/Users/rabeya/Flask_Project_Text/static/CEW_file.txt') as word_file:
    f = word_file.read()
    for line in f.split('\n'):
        common_words.append(line)


# ------------------- Main function to Summarize and keywords -------------------------
def Summarize_paper(TEXT, word_count, fraction):
    

    souped_paper = soup(TEXT.text, 'html.parser')
    paper = ''
    for my_tag in souped_paper.find_all('p'):
        paper += my_tag.text
        
    keyword_str = keywords(paper, ratio=fraction).lower()
    keyword_list = keyword_str.split('\n')
    gist = summarize(paper, word_count=word_count)
    gist = ' '.join(gist.split('\n')).replace('\xa0', '')
    tokens_gist = word_tokenize(gist)
    # here we will add more keywords by filtering common words out
    for w in tokens_gist:
        wn_tag_w = get_wordnet_pos(pos_tag([w])[0][1])
        if (w.lower() not in common_words) and (wnl.lemmatize(w.lower(), wn_tag_w) not in common_words):
            keyword_list.append(w)

    # Finalize and edit  keywords       
    keyword_set = list(set(keyword_list))
    important_words = [k for k in keyword_set if k.isalpha()]
    important_words = [iw for iw in important_words if iw not in common_words]
    #keywords_from_summary = keywords(gist, fraction).split()
    try:
        keywords_from_summary = keywords(gist, fraction).split()
    except:
        return tuple([gist, ''])
    updated_keywords = list(set(important_words + keywords_from_summary))
    tagged_kw = pos_tag((updated_keywords))
    updated_keywords = [p[0] for p in tagged_kw if p[1].isalpha() and p[1].startswith('V')==False]
    important_words_str = ', '.join(updated_keywords)

    # return the summary and keywords
    return tuple([gist, important_words_str])