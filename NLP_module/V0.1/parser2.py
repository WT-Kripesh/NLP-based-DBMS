import nltk
from nltk.corpus import stopwords
import re

synonyms_dict = {
    "fetch": "SELECT",
    "get": "SELECT",
    "display": "SELECT",
    "list": "SELECT",
    "all": "*",
    "information": "*",
    "data": "*",
    "details": "*",
    "whose": "WHERE",
    "which": "WHERE",
    "with": "WHERE",
    "greater": ">",
    "more": ">",
    "above": ">",
    "less": "<",
    "below": "<",

    "in descending order": "ORDER BY aggregate DESC",
    "in ascending order": "ORDER BY aggregate ASC",
}

def tokenize(text,n=1):
    # Tokenize the text
    text = text.lower()
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n + 1)]
    print("\nTokenized Query:\n", ngrams)
    return [ngram for ngram in ngrams if ngram.strip()] 

def discard_insignificant_tokens(tokens):
    # Discard insignificant tokens
    significant_tokens = [token for token in tokens if token not in stopwords.words('english') and re.match(r'\w+', token)]
    print("\nSignificant Tokens:\n", significant_tokens)
    return significant_tokens

def replace_with_synonyms(tokens, synonyms_dict):
    # Replace tokens with synonyms from the dictionary
    replaced_tokens = [synonyms_dict.get(token, token) for token in tokens]
    print("\nTokens Replaced with Synonyms:\n", replaced_tokens)
    return replaced_tokens


NL_query = input("Enter a query to parse\n")

# Tokenize the query
tokens = tokenize(NL_query, n=1)

# Discard insignificant tokens
significant_tokens = discard_insignificant_tokens(tokens)

# Replace tokens with synonyms
replaced_tokens = replace_with_synonyms(significant_tokens, synonyms_dict)

#print("\nFinal Tokens after Replacement:\n", replaced_tokens)

