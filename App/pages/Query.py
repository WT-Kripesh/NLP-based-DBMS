import streamlit as st
from mysql.connector import Error
import sys
sys.path.insert(1,'/Users/kripesh/Developer/Projects/NLP-based-DBMS/NLP_module')
from Query_generator import get_query

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
    selected_db = st.session_state["selected_db"]
    mycursor = connection.cursor()

    # NLP query input
    st.header("Input Your Query")

    natural_language_query = st.text_input("Enter your query in English:")
    if natural_language_query:
        sql_query = get_query(natural_language_query,mycursor,selected_db)
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

