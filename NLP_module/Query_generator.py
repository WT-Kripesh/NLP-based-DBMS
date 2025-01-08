# import sys
# sys.path.insert(0,'/Users/kripesh/Developer/Projects/NLP-based-DBMS')
from database_structure import find_total_information_of_selected_db
from database_structure import find_all_the_columns_in_a_table_from_given_database_with_datatype
from database_structure import find_all_the_columns_in_a_table_from_given_database_with_datatype
from database_connection import db_config
import re

dict_of_synonyms = {
    'select_list' : ["fetch", "get", "display", "list", "find", "show", "retrieve", "pull", "extract", "collect", "gather", "bring", "return"], 

    'from_list' : [ "from","of"],

    '*_list' : ["every", "all", "everything", "any", "each", "whole", "entire", "total"], 

    'where_list' : ["whose", "which", "with", 'where', "having", "that", "who","from"], 

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

    'desc_list' : ["descending", "highest to lowest", "largest to smallest", "biggest to smallest", "decreasing", "in descending order", "in decreasing order",],

    'asc_list' : ["ascending", "lowest to highest", "smallest to largest", "smallest to biggest", "increasing", "in ascending order", "in increasing order",]
}

symbols= [',', '/', ';', ':', '"', "'", '!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '|', '\\', '~']

def custom_unigram_tokenizer(text):
    # Regular expression to split by spaces but retain '.' in numbers
    tokens = re.split(r'(\s+)', text)  # Split by whitespace, retaining it
    
    cleaned_tokens = []
    for token in tokens:
        # Remove trailing punctuation except '.' in numbers
        if re.match(r'^\d+\.\d+$', token):
            cleaned_tokens.append(token)
        else:
            # Remove punctuation at the end of tokens
            cleaned_tokens.append(re.sub(r'[.,-]+$', '', token))
    return [t for t in cleaned_tokens if t.strip()]  # Remove empty tokens



def tokenize_the_text(text, n):
    text = text.lower()
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n + 1)]
    return [ngram for ngram in ngrams if ngram.strip()]  # Filter out empty strings


#Selection of table
#table is selected based on the NL query. 
def find_data_type_of_the_given_attribute(cursor, selected_db, from_clause, attribute):

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
def find_from_clause(tokens, list_of_tables):
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



#lets find out list of columns name which is included in the NL query
#assumption: select list ra from list ko bichmaa hunxa...

#for select clause 
def find_select_clause(list_of_column_in_selected_table, tokens):
    select_clause = []

    # 
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

    return select_clause



# print(select_clause)




#######################################################
#working for where condition



def find_where_clause(cursor, selected_db, from_clause, list_of_column_in_selected_table, tokens):
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
                # print(token)
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
            # print(temp_conditional)
            # print(type(temp_conditional))
            # print(temp_conditional)

            last_token = ''
            if ( find_data_type_of_the_given_attribute(cursor, selected_db, from_clause, attribute) != 'varchar' ):
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
            if ( find_data_type_of_the_given_attribute(cursor, selected_db, from_clause, attribute) == 'varchar' ):
                value = "\'" + value + "\'"
                print(value)
            
            where_clause_conditions.append(attribute + operator + value)
            # print(where_clause_conditions)
            
            
    final_where_clause_condition = ''
    if len(where_clause_conditions)!= 0:
        final_where_clause_condition = (' '+ selected_conjunction.upper()+' ').join(where_clause_conditions)

    return final_where_clause_condition


# print(where_clause)


#ordered by extraction
def find_ordered_by_clause(list_of_column_in_selected_table, tokens):
    ordered_by_clause_list = []

    starting_index = None

    for index, token in enumerate(tokens):  
        if token in dict_of_synonyms["ordered_by_list"]:
            starting_index = index
            break

    if (starting_index != None):
        temp_token = tokens[starting_index + 1 : len(tokens)]


        for index, token in enumerate(temp_token):
            if token in dict_of_synonyms['asc_list']:
                for i in range(index+1, len(temp_token)):
                    if temp_token[i] in list_of_column_in_selected_table:
                        ordered_by_clause_list.append((temp_token[i], 'ASC'))
                        break
        
        for index, token in enumerate(temp_token):
            if token in dict_of_synonyms['desc_list']:
                for i in range(index+1, len(temp_token)):
                    if temp_token[i] in list_of_column_in_selected_table:
                        ordered_by_clause_list.append((temp_token[i], 'ASC'))

    ordered_by_clause = ''
    for index, _tuple in enumerate(ordered_by_clause_list):
        if index == 0:
            ordered_by_clause += _tuple[0]
            ordered_by_clause += ' '+ _tuple[1]
        else:
            ordered_by_clause += ', ' + _tuple[0]
            ordered_by_clause += ' '+ _tuple[1]



    return ordered_by_clause




def get_query(NL_query, cursor,selected_db=None):
    NL_query = NL_query.lower()
    tokens = custom_unigram_tokenizer(NL_query)
    if selected_db == None:
        selected_db = db_config['database']
    selected_db_info = find_total_information_of_selected_db(selected_db, cursor)   
    list_of_tables = list( selected_db_info.keys())
    from_clause = find_from_clause(tokens, list_of_tables)
    list_of_column_in_selected_table = selected_db_info[from_clause]
    select_clause = find_select_clause(list_of_column_in_selected_table, tokens )
    where_clause = find_where_clause(cursor, selected_db, from_clause, list_of_column_in_selected_table, tokens)
    order_by_clause = find_ordered_by_clause(list_of_column_in_selected_table, tokens)

    final_query = "SELECT " + ', '.join(select_clause) + "\n" + "FROM " + from_clause
    if where_clause:
        final_query += "\n" + "WHERE " + where_clause
    if order_by_clause:
        final_query += "\n" + "ORDER BY " + order_by_clause
    return final_query

    


# NL_query = "find name, roll no and marks of the detail of students whose marks is greater than 50.5 arranged in ascending order by name and in ascending order by marks."
# query = get_query(NL_query)
# print(query)