
#list of inbuilt system databases to ignore
system_databases = ['information_schema', 'mysql', 'performance_schema', 'sys']

#fetch all databases in local DBMS
def find_all_databases(cursor):
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    list_of_databases = [db[0] for db in databases if db[0] not in system_databases]
    return list_of_databases

def find_all_the_tables_in_a_database(database_name,cursor):
    cursor.execute(f"USE {database_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    return tables


def find_all_the_columns_in_a_table_from_given_database(database_name, table_name,cursor):
    cursor.execute(f"USE {database_name}")
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    columns = [column[0] for column in columns]
    return columns

def fetch_total_information(list_of_databases, cursor):
    total_information_dict = {}
    for db in list_of_databases:
        table_columns_dict = {}
        all_tables_in_db = find_all_the_tables_in_a_database(db,cursor)
        for table in all_tables_in_db:
            table_columns_dict[table] = find_all_the_columns_in_a_table_from_given_database(db,table,cursor)
        total_information_dict[db] = table_columns_dict
    return total_information_dict

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