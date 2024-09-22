import re

dict_of_synonyms = {
    'select_list' : ["fetch", "get", "display", "list", "find", "show", "retrieve", "pull", "extract", "collect", "gather", "bring", "return"], 
    'from_list' : ["from", "of"],
    '*_list' : ["every", "all", "everything", "any", "each", "whole", "entire", "total"], 
    'where_list' : ["whose", "which", "with", 'where', "having", "that", "who", "in which", "for which", "by which", "through which", "on which"], 
    '>_list' : ["more", "above", "greater", "exceeding", "over", "higher", "larger", "superior", "bigger", "exceeds", "exceed", "greater than"], 
    '<_list' : ["less", "below", "lesser", "under", "lower", "smaller", "inferior", "fewer", "underneath", "smaller than"],
    '>=_list' : ["at least", "no less than", "greater than or equal to", "not less than", "minimum of", "more or equal", "more than or equal to"],
    '<=_list' : ["at most", "no more than", "less than or equal to", "not more than", "maximum of", "less or equal", "less than or equal to"],
    '=__list' : ["equals", "equal to", "is", "are", "was", "were", "is equal to", "is exactly", "exactly", "equals to"],
    '!=_list' : ["not equal to", "does not equal", "is not", "are not", "isn't", "aren't", "not the same as", "differs from", "unequal", "is different from"],
    'and_list' : ["and", "as well as", "also", "both", "along with", "together with", "plus", "additionally", "in addition to", "with", "coupled with"],
    'or_list' : ["or", "either", "alternatively", "otherwise", "in place of", "in lieu of", "as an alternative", "instead of", "else"],
    'order_by_list' : ["arrange by", "sort by", "order by", "ordered by", "sorted by", "sequence by", "arranged by", "in the order of", "organize by", "rank by"],
    'group_by_list' : ["group by", "categorized by", "classified by", "clustered by", "partitioned by", "segregated by", "divided by", "bunched by"],
    'sum_list' : ["total", "sum", "summed up", "aggregate", "totalled", "added up", "summation", "cumulative"],
    'avg_list' : ["average", "mean", "median", "norm", "standard", "middle", "typical", "usual", "ordinary", "expected value"],
    'min_list' : ["minimum", "least", "smallest", "lowest", "minimal", "fewest", "slightest", "tiniest", "shortest", "bottom"],
    'max_list' : ["maximum", "greatest", "largest", "highest", "most", "top", "biggest", "utmost", "supreme", "pinnacle"],
    'count_list' : ["count", "number of", "frequency of", "amount", "total number", "sum of", "tally", "quantity", "enumerate"],
    'like_list' : ["like", "similar to", "matches", "contains", "resembling", "alike", "akin to", "such as", "comparable to", "close to"],
    'not_like_list' : ["not like", "does not match", "does not contain", "unlike", "different from", "not similar to", "not containing", "dissimilar to"],
    'in_list' : ["in", "within", "among", "included in", "inside", "part of", "contained in", "amidst", "amongst", "included among"],
    'not_in_list' : ["not in", "not included in", "excluded from", "outside", "not part of", "not within", "not among", "not contained in"]
}

exception =  {
    'DESC' : ["descending", "highest to lowest", "largest to smallest", "biggest to smallest", "decreasing", "in descending order", "in decreasing order", "from highest to lowest", "from largest to smallest"],
    'ASC' : ["ascending", "lowest to highest", "smallest to largest", "smallest to biggest", "increasing", "in ascending order", "in increasing order", "from lowest to highest", "from smallest to largest"]
}
keywords = ['*', ]
connectives = ["and" , "or"]
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
words_required_from_stopwords = ['from', 'is','and', 'or', 'not', 'where', 'greater', 'lesser', 'all', 'above', 'below','which', 'who', 'whom', "of", "by", "with","more"]

stopwords = [word for word in stopwords if word not in words_required_from_stopwords]

def find_synonyms(word):
    for key in dict_of_synonyms:
        if word in dict_of_synonyms[key]:
            return key.rsplit('_', 1)[0].replace('_', ' ').upper()
    for key in exception:
        if word in exception[key]:
            return key
    aggregate_functions = ['sum', 'average', 'count', 'min', 'max']
    if word in aggregate_functions:
        return word.upper()
    return word

def tokenize(text, n=1):
    text = text.lower()
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n + 1)]
    return [ngram for ngram in ngrams if ngram.strip()]

def discard_insignificant_tokens(tokens):
    return [token for token in tokens if token not in stopwords and re.match(r'\w+', token)]

def replace_with_synonyms(tokens):
    return [find_synonyms(token) for token in tokens]

def construct_sql_query(tokens):
    select_clause = []
    from_clause = ""
    where_clause = []
    order_by_clause = ""
    for i, token in enumerate(tokens):
        if token == 'SELECT':
            select_clause.append(tokens[i+1])
        elif token == 'FROM':
            # print(tokens[i+1])
            # print(find_synonyms(tokens[i+1]))
            # from_clause = tokens[i+1] if find_synonyms(tokens[i+1]) == tokens[i+1] else tokens[i+2]
            # from_clause = tokens[i+1] if find_synonyms(tokens[i+1]) == tokens[i+1] else tokens[i+2]
            for x in range(i+1, len(tokens)):
                # print(tokens[x])
                if tokens[x] not in keywords:
                    from_clause = tokens[x]
                    break
        elif token == 'WHERE':
            condition = " ".join(tokens[i+1:i+5])
            # for x in range(i+1, tokens.index('AND')):
            #     condition = " ".join(tokens[x])
            # for x in range(tokens.index('AND')+1, len):
            #     condition = " ".join(tokens[x])
            where_clause.append(condition)
        elif token.upper() == "SORT":
            order_by_clause = tokens[i+1] + ' ' + tokens[i+2]
            print(order_by_clause)
    
    query = f"SELECT {', '.join(select_clause)} FROM {from_clause}"
    if where_clause:
        query += f" WHERE {' AND '.join(where_clause)}"
    if order_by_clause:
        query += f" ORDER BY {order_by_clause}"

    return query

def get_query(NL_query):
    tokens = tokenize(NL_query, n=1)
    significant_tokens = discard_insignificant_tokens(tokens)
    print(significant_tokens)
    
    replaced_tokens = replace_with_synonyms(significant_tokens)
    print(replaced_tokens)
    
    sql_query = construct_sql_query(replaced_tokens) + ';'
    print("\n","-"*50)
    print(sql_query)
    # print("\n","*"*100)
    return sql_query

# NL_query = input("Enter your query. ")
# print(get_query(NL_query))

#       find all of the student who have marks greater than 80.
#       Get me the name of the student whose age is 22.