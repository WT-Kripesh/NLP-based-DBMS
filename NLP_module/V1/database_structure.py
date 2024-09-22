# objective is to make datastructure like this which holds entire information needed for further analysis...
# it is a nested dictionary structure. 

# {
#     'database1' : 
#     {
#         'table1' : ['col1', 'col2', 'col3'] ,
#         'table2' : ['col1', 'col2', 'col3'] ,
#         'table3' : ['col1', 'col2', 'col3'] ,
#     },
#     'database2' : 
#     {
#         'table1' : ['col1', 'col2', 'col3'] ,
#         'table2' : ['col1', 'col2', 'col3'] ,
#         'table3' : ['col1', 'col2', 'col3'] ,
#     },
# }

import mysql.connector
import re


# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="Root@55261"  # Replace with your MySQL password
)

cursor = connection.cursor()

# Fetch all databases
cursor.execute("SHOW DATABASES")

databases = cursor.fetchall()
# print(databases)

# List of system databases to ignore
system_databases = ['information_schema', 'mysql', 'performance_schema', 'sys']

# print("Databases :")
list_of_databases = [db[0] for db in databases if db[0] not in system_databases]
# print(list_of_databases)

def find_all_the_tables_in_a_database(database_name,cursor):
    cursor.execute(f"USE {database_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    # print(tables)
    tables = [table[0] for table in tables]
    return tables

# print(find_all_the_tables_in_a_database('nlpdemo'), cursor)


def find_all_the_columns_in_a_table_from_given_database(database_name, table_name, cursor):
    cursor.execute(f"USE {database_name}")
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    # print(columns)
    columns = [column[0] for column in columns]
    return columns

def find_all_the_columns_in_a_table_from_given_database_with_datatype(database_name, table_name, cursor):
    cursor.execute(f"USE {database_name}")
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    # print(columns)
    columns_with_datatype = []
    for column in columns:
        column = list(column)
        column[1] = re.sub(r'[^a-zA-Z]', '', column[1])
        columns_with_datatype.append({column[0] : column[1]})
    return columns_with_datatype



# print(find_all_the_columns_in_a_table_from_given_database_with_datatype('nlpdemo', 'students'))
# print(find_all_the_columns_in_a_table_from_given_database('nlpdemo', 'students'))
# print(find_all_the_columns_in_a_table_from_given_database('nlpdemo', 'employee',cursor))


total_information = {}
for db in list_of_databases:

    table_columns_dictionary = {}
    all_tables_in_db = find_all_the_tables_in_a_database(db,cursor)
    for table in all_tables_in_db:
        table_columns_dictionary[table] = find_all_the_columns_in_a_table_from_given_database(db, table, cursor)
    
    total_information[db] = table_columns_dictionary

#print(total_information)

#for key,value in total_information.items():
#    print()
#    print(f"{key}:{value}")
   

#variables: total_information









# for db in databases:
#     if db[0] not in system_databases:
#         print(f"\nDatabase: {db[0]}")
        
#         # Switch to each user-created database
#         cursor.execute(f"USE {db[0]}")
        
#         # Fetch all tables in the current database
#         cursor.execute("SHOW TABLES")
#         tables = cursor.fetchall()
#         print(tables)
        
#         for table in tables:
#             print(f"  Table: {table[0]}")
            
#             # Fetch all columns in the current table
#             cursor.execute(f"DESCRIBE {table[0]}")
#             columns = cursor.fetchall()
            
#             print("    Columns:")
#             for column in columns:
#                 print(f"      {column[0]} - {column[1]}")  # Column name and type


# Close the connection
cursor.close()
connection.close()
