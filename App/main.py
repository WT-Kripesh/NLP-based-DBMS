import streamlit as st

def main():
    st.set_page_config(page_title="NLP-Based DBMS", layout="wide")
    st.title("Welcome to NLP-Based DBMS")
    
    # Promotional and informative content
    st.header("About Our Project")
    st.write("""
        Our NLP-based DBMS simplifies database querying by allowing users to input natural language queries.
        It interprets the queries, processes them, and returns accurate results from the SQL database.
    """)

    st.header("Meet the Developers")
    st.write("""
        - Developer 1: [Name and Role]
        - Developer 2: [Name and Role]
        - Developer 3: [Name and Role]
    """)

    st.header("Key Features")
    st.markdown("""
    - Intuitive interface for natural language database querying
    - Easy SQL database configuration
    - Fast and reliable results
    """)

    st.header("How It Works")
    st.write("""
        1. Configure your database using a SQL file.
        2. Input your query in English.
        3. Get results instantly!
    """)

    st.markdown("""
        ### Let's get started by navigating to the Configuration page!
    """)
    
if __name__ == "__main__":
    main()
