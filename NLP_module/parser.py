import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re

# Download necessary NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Define a dictionary to replace tokens with synonyms that fit SQL structure
synonyms_dict = {
    "fetch": "SELECT",
    # "get","display","list": "SELECT"
    "all": "*",
    "information": "*",
    "whose": "WHERE",
    "greater": ">",
    "less": "<",
}

def tokenize(text,n=1):
    # Tokenize the text
    #tokens = word_tokenize(text.lower())
    #print("Tokenized Query:\n", tokens)
    #return tokens
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

#def map_to_sql(tokens):
    # Combine tokens to form the SQL query
    sql_query = ' '.join(tokens)
    # Handling special cases for synonyms like "greater than"
    sql_query = sql_query.replace("greater than", ">")
    print("Final SQL Query:", sql_query)
    return sql_query


NL_query = input("Enter a query to parse:\n")

# Tokenize the query
tokens = tokenize(NL_query)

# Discard insignificant tokens
significant_tokens = discard_insignificant_tokens(tokens)

# Replace tokens with synonyms
replaced_tokens = replace_with_synonyms(significant_tokens, synonyms_dict)

# Map to SQL query
#final_query = map_to_sql(replaced_tokens)

# print("\nFinal SQL Query:", final_query)
