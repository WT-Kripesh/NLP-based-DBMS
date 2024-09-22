from NLP_module.database_structure import total_information
from NLP_module.database_structure import find_all_the_columns_in_a_table_from_given_database_with_datatype


import mysql.connector
import re

# dict_of_synonyms = {
#     'select_list' : ["fetch", "get", "display", "list", "find", "show", "retrieve", "pull", "extract", "collect", "gather", "bring", "return"], 
#     'from_list' : ["from", "of"],
#     '*_list' : ["every", "all", "everything", "any", "each", "whole", "entire", "total"], 
#     'where_list' : ["whose", "which", "with", 'where', "having", "that", "who"], 
#     '>_list' : ["more", "above", "greater", "exceeding", "over", "higher", "larger", "superior", "bigger", "exceeds", "exceed", "greater than"], 
#     '<_list' : ["less", "below", "lesser", "under", "lower", "smaller", "inferior", "fewer", "underneath", "smaller than"],
#     '>=_list' : ["at least", "no less than", "greater than or equal to", "not less than", "minimum of", "more or equal", "more than or equal to"],
#     '<=_list' : ["at most", "no more than", "less than or equal to", "not more than", "maximum of", "less or equal", "less than or equal to"],
#     '=__list' : ["equals", "equal to", "is", "are", "was", "were", "is equal to", "is exactly", "exactly", "equals to"],
#     '!=_list' : ["not equal to", "does not equal", "is not", "are not", "isn't", "aren't", "not the same as", "differs from", "unequal", "is different from"],
#     'and_list' : ["and", "as well as", "also", "both", "along with", "together with", "plus", "additionally", "in addition to", "with", "coupled with"],
#     'or_list' : ["or", "either", "alternatively", "otherwise", "in place of", "in lieu of", "as an alternative", "instead of", "else"],
#     'order_by_list' : ["arrange by", "sort by", "order by", "ordered by", "sorted by", "sequence by", "arranged by", "in the order of", "organize by", "rank by"],
#     'group_by_list' : ["group by", "categorized by", "classified by", "clustered by", "partitioned by", "segregated by", "divided by", "bunched by"],
#     'sum_list' : ["total", "sum", "summed up", "aggregate", "totalled", "added up", "summation", "cumulative"],
#     'avg_list' : ["average", "mean", "median", "norm", "standard", "middle", "typical", "usual", "ordinary", "expected value"],
#     'min_list' : ["minimum", "least", "smallest", "lowest", "minimal", "fewest", "slightest", "tiniest", "shortest", "bottom"],
#     'max_list' : ["maximum", "greatest", "largest", "highest", "most", "top", "biggest", "utmost", "supreme", "pinnacle"],
#     'count_list' : ["count", "number of", "frequency of", "amount", "total number", "sum of", "tally", "quantity", "enumerate"],
#     'like_list' : ["like", "similar to", "matches", "contains", "resembling", "alike", "akin to", "such as", "comparable to", "close to"],
#     'not_like_list' : ["not like", "does not match", "does not contain", "unlike", "different from", "not similar to", "not containing", "dissimilar to"],
#     'in_list' : ["in", "within", "among", "included in", "inside", "part of", "contained in", "amidst", "amongst", "included among"],
#     'not_in_list' : ["not in", "not included in", "excluded from", "outside", "not part of", "not within", "not among", "not contained in"]
# }

#redefined dict_of_synonyms
dict_of_synonyms = {
    'select_list' : ["fetch", "get", "display", "list", "find", "show", "retrieve", "pull", "extract", "collect", "gather", "bring", "return"], 

    'from_list' : ["from", "of"],

    '*_list' : ["every", "all", "everything", "any", "each", "whole", "entire", "total"], 

    'where_list' : ["whose", "which", "with", 'where', "having", "that", "who"], 

    '>_list' : ["more", "above", "greater", "exceeding", "over", "higher", 
    "larger", "superior", "bigger", "exceeds", "exceed", "greater than"], 

    '<_list' : ["less than", "below", "lesser than", "under", "lower than", "smaller than", "inferior", "fewer", "underneath", "smaller", "less"],

    '>=_list' : ["at least", "no less than", "greater than or equal to", "not less than", "minimum of", "more or equal", "more than or equal to"],

    '<=_list' : ["at most", "no more than", "less than or equal to", "not more than", "maximum of", "less or equal", "less than or equal to"],

    '=_list' : ["equals", "equal to", "is", "are", "was", "were", "is equal to", "is exactly", "exactly", "equals to"],

    '!=_list' : ["not equal", "is not", "are not", "isn't", "aren't", "unequal"],

    'and_list' : ["and"],

    'or_list' : ["or"],

    'ordered_by_list' : ["arranged", "ordered"],

    'desc_list' : ["descending", "highest to lowest", "largest to smallest", "biggest to smallest", "decreasing", "in descending order", "in decreasing order", "from highest to lowest", "from largest to smallest"],

    'asc_list' : ["ascending", "lowest to highest", "smallest to largest", "smallest to biggest", "increasing", "in ascending order", "in increasing order", "from lowest to highest", "from smallest to largest"]
}


stopwords = []
with open('english_stopwords.txt') as stopwords_file:
    for line in stopwords_file:
        # print(line, end='')
        line = line.replace('\n', '')
        stopwords.append(line)

#old stopwords
# stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
# words_required_from_stopwords = ['from', 'is','and', 'or', 'not', 'where', 'greater', 'lesser', 'all', 'above', 'below','which', 'who', 'whom', "of", "by", "with","more"]
# stopwords = [word for word in stopwords if word not in words_required_from_stopwords]



# NL_query = input("Enter your query in English. ").lower()
# NL_query = "Find the name, age and salary of the employee whose salary is greater than 50 and less than 30."
# NL_query = "Find the name, age and salary of the employee whose salary is greater than 50 and less than 30 ordered in ascending order. "
# NL_query = "Find the name, age and salary of the emp whose salary is greater than 50 or whose name is Binod ordered in ascending order. "ss
# NL_query = "Find the students having marks greater than 50."
# NL_query = "find all of the students whose marks is greater than 50"
NL_query = "find all of the detail of students."


NL_query = NL_query.lower()



symbols= [',', '/', ';', ':', '"', "'", '!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '|', '\\', '~']
tokens = []
for word in NL_query.split():
    if word not in symbols:
        for symbol in symbols:
            if symbol in word:
                word = word.replace(symbol, '')
        tokens.append(word)

def tokenize_the_text(text, n):
    text = text.lower()
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n + 1)]
    return [ngram for ngram in ngrams if ngram.strip()]  # Filter out empty strings

# tokens has been generated in tokens variable.
# print(tokens)

#lets select a database first
selected_db = 'nlpdemo'

#lets extract table first
#stores tables and columns information about selected_db, it is in dictionary format where keys are table name and value is a list which contains list of columns/attributes
selected_db_info = total_information[selected_db]   

#list of tables in selected dB
list_of_tables = list( selected_db_info.keys() )
# print(list_of_tables)






# print(list_of_tables)

#Selection of table
#table is selected based on the NL query. 


def extract_value(text, keyword):
    # Create regex pattern to match the keyword followed by a word/number, allowing for ending punctuation
    pattern = rf'{keyword} (\w+|\d+)[\s,.]'
    match = re.search(pattern, text)
    
    # If there’s no trailing space, comma, or period, adjust the pattern
    if not match:
        pattern = rf'{keyword} (\w+|\d+)$'  # Match at the end of the string
        match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    return None

def longest_common_subsequence(s1, s2):
    # Initialize a 2D array to store lengths of longest common subsequence
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # The length of the longest common subsequence is in dp[m][n]
    lcs_length = dp[m][n]

    # Reconstruct the LCS string
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    # The LCS list is built backwards, so reverse it
    lcs.reverse()
    lcs_string = ''.join(lcs)

    return lcs_length, lcs_string

#word 1 should always be lcs, word2 should be entinty name

def find_data_type_of_the_given_attribute(attribute):
# Database configuration with credentials  :   change it if necessary
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Root@55261',                         
    }

    # Establish database connection

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    columns_with_datatype = find_all_the_columns_in_a_table_from_given_database_with_datatype(selected_db, from_clause, cursor)

    idx = None
    found = False

    for index, item in enumerate(columns_with_datatype):
        for key in item.keys():
            if key == attribute:
                idx = index
                found = True
                break  # Break the inner loop
        if found:
            break  # Break the outer loop
    
    return (list(columns_with_datatype[idx].values()))[0]

# print(type(find_data_type_of_the_given_attribute('salary')))

def find_neighbour_similarity_count(word1, word2):
    count = 0
    len1 = len(word1)
    len2 = len(word2)

    # They can't be similar if len is 0 or 1.
    if len1 < 2 or len2 < 2:
        return count
    
    # let word1 be lcs and word2 be column.
    # we are checking how close lcs can get to column
    for index1, letter1 in enumerate(word1):
        for index2, letter2 in enumerate(word2):
            # print(letter1)
            if index1 == 0:
                # Ensure next character exists before accessing index1 + 1 and index2 + 1
                if letter1 == letter2 and index1 + 1 < len1 and index2 + 1 < len2 and word1[index1 + 1] == word2[index2 + 1]:
                    count += 0.5
                    # print("condition 1 is executed.")
                    break

            elif index2 == 0:
                # print("condition 2 is executed.")
                continue

            elif index1 == len1 - 1:
                # Ensure previous character exists before accessing index1 - 1 and index2 - 1
                if letter1 == letter2 and index1 - 1 >= 0 and index2 - 1 >= 0 and word1[index1 - 1] == word2[index2 - 1]:
                    count += 0.5
                    # print("condition 3 is executed.")
                    break

            elif index2 == len2 - 1:
                break

            elif letter1 == letter2:
                if (index1 - 1 >= 0 and index2 - 1 >= 0 and word1[index1 - 1] == word2[index2 - 1] and
                    index1 + 1 < len1 and index2 + 1 < len2 and word1[index1 + 1] == word2[index2 + 1]):
                    # print("condition 4 is executed.")
                    count += 1
                    break

                elif (index1 - 1 >= 0 and index2 - 1 >= 0 and word1[index1 - 1] == word2[index2 - 1]):
                    # print("condition 5 is executed.")
                    count += 0.5
                    break

                elif (index1 + 1 < len1 and index2 + 1 < len2 and word1[index1 + 1] == word2[index2 + 1]):
                    # print("condition 6 is executed.")
                    count += 0.5
                    break

    return count


# selected_table = ''
def select_table(tokens, list_of_tables):
    count_info_of_table = {}
    for table in list_of_tables:
        count_info_of_token = {}

        for token in tokens:
            # print(f"token: {token} , table: {table}")
            lcs =  longest_common_subsequence(token, table)[1]
            table_neighbour_similarity_count = find_neighbour_similarity_count(lcs, table)
            count_info_of_token[token] = table_neighbour_similarity_count
        
        # print(count_info_of_token)
        count_info_of_table[table] = max(count_info_of_token.values())
        # print(count_info_of_table[table])

    # print(count_info_of_table)
    max_count = max(count_info_of_table.values())
    # print(max_count)

    for table, value in count_info_of_table.items():
        if value == max_count:
            selected_table = table  
    
    return selected_table



from_clause = select_table(tokens, list_of_tables)
# print(from_clause)



#lets find out list of columns name which is included in the NL query







#assumption: select list ra from list ko bichmaa hunxa...
#for select clause 
select_clause = []

list_of_column_in_selected_table = selected_db_info[from_clause]
# print(list_of_column_in_selected_table)
starting_index = 0
ending_index = 0
for index, token in enumerate(tokens):
    if token in dict_of_synonyms["select_list"]:
        starting_index = index + 1
    
    if token in dict_of_synonyms["from_list"]:
        ending_index = index - 1


candidate_token = tokens[starting_index:ending_index+1]
# print(candidate_token)


for token in candidate_token:
    for column in list_of_column_in_selected_table:
        # lcs = longest_common_subsequence(column, token)[1]
        # print(lcs)
        neighbout_count = find_neighbour_similarity_count(token, column)

        if neighbout_count >= 2:
            select_clause.append(column)

if len(select_clause) == 0:
    select_clause.append('*')








#######################################################
#working for where condition




where_clause_conditions = []

starting_index = None
for index, token in enumerate(tokens):
    if token in dict_of_synonyms["where_list"]:
        starting_index = index + 1
        break
    
ending_index = None
for index, token in enumerate(tokens):  
    if token in dict_of_synonyms["ordered_by_list"]:
        ending_index = index - 1
        break

if (ending_index == None):
    ending_index = len(tokens) - 1

if starting_index != None:
    where_tokens = tokens[starting_index:ending_index+1]

    # each experession contains attribute, operator and value
    # i.e salary > 50

    # print(where_tokens)
    list_of_possible_conjunctions = ['and', 'or']

    selected_conjunction = ''
    # print(list_of_possible_conjunctions)

    for conjunction in list_of_possible_conjunctions:
        if conjunction in where_tokens:
            selected_conjunction = conjunction
            break

    conditional_tokens = []
    if(len(selected_conjunction) != 0):
        # print("true")
        conditional_token1 = []
        conditional_token2 = []
        
        conjunction_appearing_flag = False

        for token in where_tokens:
            if token == selected_conjunction:
                conjunction_appearing_flag = True
                continue
            
            if conjunction_appearing_flag == False:
                conditional_token1.append(token)
            else:
                conditional_token2.append(token)

        # print(conditional_token1)
        # print(conditional_token2)

        conditional_tokens.append(conditional_token1)
        conditional_tokens.append(conditional_token2)
    else:
        conditional_tokens.append(where_tokens)


    last_attribute = None
    for conditional in conditional_tokens:
        attribute = None
        operator = ''
        value = ''

        #attribute selection
        for token in conditional:
            print(token)
            # for column in list_of_column_in_selected_table:
            if token in list_of_column_in_selected_table:
                attribute = token
                last_attribute = attribute
                # print(attribute)
                break
        if attribute == None:
            attribute = last_attribute

            #     neighbout_count = find_neighbour_similarity_count(token, column)

            #     if neighbout_count >= 3:
            #         attribute = column
            #         break
            # if (attribute != ''):
            #     break

        # conditional.remove(attribute)
        # print(attribute)
        # print(conditional)
        
    
    

        #operator selection
        
        operator_selected_flag = False
    
    
        #check for >=
        temp_conditional = ' '.join(conditional)
        print(temp_conditional)
        # print(type(temp_conditional))
        # print(temp_conditional)

        last_token = ''
        if ( find_data_type_of_the_given_attribute(attribute) != 'varchar' ):
            for i in range(5,1,-1):
                if (len(temp_conditional) < i):
                    continue
                
                
                temp_token = tokenize_the_text(temp_conditional, i)
                for token in temp_token:
                    if token in dict_of_synonyms['>=_list']:
                        operator = '>='
                        last_token = token
                        operator_selected_flag = True
                        break
                if operator_selected_flag == True:
                    break

            #check for <=
            if operator_selected_flag == False:
                for i in range(5,1,-1):
                    if (len(temp_conditional) < i):
                        continue


                    temp_token = tokenize_the_text(temp_conditional, i)
                    for token in temp_token:
                        if token in dict_of_synonyms['<=_list']:
                            operator = '<='
                            last_token = token
                            operator_selected_flag = True
                            break
                    if operator_selected_flag == True:
                        break

            #check for <
            if operator_selected_flag == False:
                for i in range(2,0,-1):
                    if (len(temp_conditional) < i):
                        continue
                    temp_token = tokenize_the_text(temp_conditional, i)
                    for token in temp_token:
                        if token in dict_of_synonyms['<_list']:
                            operator = '<'
                            last_token = token
                            operator_selected_flag = True
                            break
                    if operator_selected_flag == True:
                        break

            #check for >
            if operator_selected_flag == False:
                for i in range(2,0,-1):
                    if (len(temp_conditional) < i):
                        continue
                    temp_token = tokenize_the_text(temp_conditional, i)
                    for token in temp_token:
                        if token in dict_of_synonyms['>_list']:
                            operator = '>'
                            last_token = token
                            operator_selected_flag = True
                            break
                    if operator_selected_flag == True:
                        break

        #check for !=
        if operator_selected_flag == False:
            for i in range(2,0,-1):
                if (len(temp_conditional) < i):
                    continue
                temp_token = tokenize_the_text(temp_conditional, i)
                for token in temp_token:
                    if token in dict_of_synonyms['!=_list']:
                        operator = '!='
                        last_token = token
                        operator_selected_flag = True
                        break
                if operator_selected_flag == True:
                    break

        #check for =
        if operator_selected_flag == False:
            for i in range(3,0,-1):
                if (len(temp_conditional) < i):
                    continue
                temp_token = tokenize_the_text(temp_conditional, i)
                for token in temp_token:
                    if token in dict_of_synonyms['=_list']:
                        operator = '='
                        last_token = token
                        operator_selected_flag = True
                        break
                if operator_selected_flag == True:
                    break
        
        # print(operator)

        #value selection/extraction
        # print(temp_conditional)
        # print(last_token)

        value = extract_value(temp_conditional, last_token)
        # print(value)
        
        where_clause_conditions.append(attribute + operator + value)
        # print(where_clause_conditions)
        
        
final_where_clause_condition = ''
if len(where_clause_conditions)!= 0:
    final_where_clause_condition = (' '+ selected_conjunction.upper()+' ').join(where_clause_conditions)

#ordered by extraction

print(final_where_clause_condition)

if(len(final_where_clause_condition) != 0):
    print(f"""
            SELECT {', '.join(select_clause)}
            FROM {from_clause}
            WHERE {final_where_clause_condition}
            """)
else:
    print(f"""
            SELECT {', '.join(select_clause)}
            FROM {from_clause}
            """)
