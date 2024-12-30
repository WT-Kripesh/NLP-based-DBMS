import streamlit as st
from streamlit_lottie import st_lottie

def main():
    st.set_page_config(page_title="NLP-Based DBMS",initial_sidebar_state='collapsed',menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    })

    c1,c2 = st.columns(2)
    with c2:
        st.text('')
        st.text('') 
        st.text('') 
        st.text('') 
        st.text('') 
        st.title("\n\nNLP Based DBMS")
        st.write(""" A natural language interface to SQL databases.""")
    with c1:
        st_lottie("https://lottie.host/67ccc844-7aeb-4d60-9eec-4f8ff8c12dfc/82SezLULZG.json", height=400, width=300,loop=True)

# Promotional and informative content
    st.header("About Our Project")
    st.write("""
        Our NLP-based DBMS simplifies database querying by allowing users to input natural language queries.
        It interprets the queries, processes them, and returns accurate results from the SQL database.
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
    
    st.header("Meet the Developers")
    st.write("""
        - Avahan Tamrahkar [Application developer]
        - Javed Ansari [NLP engineer]
        - Kripesh Nihure [Web developer]
    """)
    st.markdown("""
        ### Let's get started by navigating to the Configuration page!
    """)
    if st.button('Start querying!'):
        st.switch_page("pages/Configuration.py")
    
if __name__ == "__main__":
    main()
