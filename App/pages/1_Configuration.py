# import streamlit as st
# import sqlite3
# import os

# def main():
#     st.title("SQL Database Configuration")

#     # Upload SQL file
#     st.header("Upload Your SQL File")
#     uploaded_file = st.file_uploader("Choose a SQL file", type=["sql"])
#     if uploaded_file:
#         sql_file_path = os.path.join("uploaded_sql_files", uploaded_file.name)
#         with open(sql_file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success(f"File {uploaded_file.name} uploaded successfully.")

#     # Predefined databases
#     st.header("Choose From Predefined Options")
#     databases = ["SampleDB1", "SampleDB2", "SampleDB3"]
#     selected_db = st.selectbox("Select a database", databases)
#     if st.button("Load Selected Database"):
#         st.success(f"Database {selected_db} loaded successfully!")

#     # Establish SQLite connection
#     st.header("Test Database Connection")
#     db_path = st.text_input("Enter database path:")
#     if st.button("Test Connection"):
#         try:
#             conn = sqlite3.connect(db_path)
#             st.success("Database connection established successfully!")
#             conn.close()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")

# if __name__ == "__main__":
#     main()

import streamlit as st
import mysql.connector

def connect_to_server(host, user, password):
    """Function to connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        return connection
    except mysql.connector.Error as e:
        return str(e)

def fetch_databases(connection):
    """Fetch all databases available for the user."""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        return databases
    except mysql.connector.Error as e:
        return str(e)

def main():
    st.title("SQL Database Configuration")

    # Database connection form
    st.header("Enter MySQL Server Credentials")
    host = st.text_input("Host", value="localhost")
    user = st.text_input("User")
    password = st.text_input("Password", type="password")

    if st.button("Connect to Server"):
        connection = connect_to_server(host, user, password)
        if isinstance(connection, str):
            st.error(f"Connection failed: {connection}")
        else:
            st.success("Connected to the MySQL server successfully!")
            st.session_state["server_connection"] = connection

            # Fetch available databases
            databases = fetch_databases(connection)
            if isinstance(databases, str):
                st.error(f"Failed to fetch databases: {databases}")
            else:
                st.session_state["databases"] = databases
                st.info("Select a database from the dropdown below.")
    
    # Display database selection dropdown if connection is successful
    if "databases" in st.session_state:
        database = st.selectbox("Available Databases", st.session_state["databases"])
        if st.button("Select Database"):
            try:
                server_connection = st.session_state["server_connection"]
                db_connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                st.session_state["db_connection"] = db_connection
                st.success(f"Database '{database}' selected successfully!")
            except mysql.connector.Error as e:
                st.error(f"Failed to connect to the database: {e}")

if __name__ == "__main__":
    main()

