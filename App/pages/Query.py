# import streamlit as st
# import sqlite3
# from transformers import pipeline

# def main():
#     st.title("Query Input and Result")

#     # Input database path
#     st.header("Database Connection")
#     db_path = st.text_input("Enter the path to your database:")
#     conn = None
#     if db_path:
#         try:
#             conn = sqlite3.connect(db_path)
#             st.success("Connected to the database successfully!")
#         except Exception as e:
#             st.error(f"Failed to connect: {e}")

#     # NLP query input
#     st.header("Input Your Query")
#     query = st.text_input("Enter your query in English:")
#     if query and conn:
#         try:
#             # Dummy NLP-to-SQL mapping
#             sql_query = f"SELECT * FROM table WHERE column LIKE '%{query}%'"
#             st.code(sql_query, language="sql")
#             cursor = conn.execute(sql_query)
#             results = cursor.fetchall()
#             st.write("Results:")
#             st.write(results)
#         except Exception as e:
#             st.error(f"Query failed: {e}")

#     # Close database connection
#     if conn:
#         conn.close()

# if __name__ == "__main__":
#     main()

import streamlit as st
from mysql.connector import Error

# Placeholder for query generation function
def generate_sql_query(natural_language_query):
    """
    This function converts a natural language query into SQL query.
    Replace this with your existing implementation.
    """
    return "SELECT * FROM table_name WHERE column_name LIKE '%value%'"

def execute_query(connection, sql_query):
    """Function to execute an SQL query."""
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    except Error as e:
        return str(e)

def main():
    st.title("Query Input and Result")

    # Check if database connection exists in session state
    if "db_connection" not in st.session_state:
        st.warning("Please configure the database connection first.")
        return

    connection = st.session_state["db_connection"]

    # NLP query input
    st.header("Input Your Query")
    natural_language_query = st.text_input("Enter your query in English:")
    if natural_language_query:
        sql_query = generate_sql_query(natural_language_query)
        st.code(sql_query, language="sql")
        
        if st.button("Execute Query"):
            results = execute_query(connection, sql_query)
            if isinstance(results, str):
                st.error(f"Query execution failed: {results}")
            else:
                st.write("Results:")
                st.write(results)

if __name__ == "__main__":
    main()

