import streamlit as st
import mysql.connector
import time

def connect_to_server(host, user, password,database=None):
    """Function to connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        return str(e)

def fetch_databases(connection):
    """Fetch all databases available for the user."""
    system_databases = ['information_schema', 'mysql', 'performance_schema', 'sys']
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall() if db[0] not in system_databases]
        return databases
    except mysql.connector.Error as e:
        return str(e)

def main():
    st.title("SQL Database Configuration")

    # Database connection form
    st.header("Enter MySQL Server Credentials")
    
    host_name = st.text_input("Host", value="localhost")
    user_name = st.text_input("User")
    passwd = st.text_input("Password", type="password")

    if st.button("Connect to Server"):
        connection = connect_to_server(host_name, user_name, passwd)
        if isinstance(connection, str):
            st.error(f"Connection failed: {connection}")
        else:
            st.success("Connected established!")

            # Fetch available databases
            databases = fetch_databases(connection)
            if isinstance(databases, str):
                st.error(f"Failed to fetch databases: {databases}")
            else:
                st.session_state["databases"] = databases
                st.info("Select a database from the dropdown below.")

                
    # Display database selection dropdown if connection is successful
    if 'databases' in st.session_state:
        db = st.selectbox("Available Databases", st.session_state["databases"])
        if st.button("Select Database"):
            try:
                db_connection = connect_to_server(host_name,user_name,passwd,db)
                st.session_state["db_connection"] = db_connection
                st.session_state['selected_db'] = db
                st.success(f"Database '{db}' selected successfully!")
                time.sleep(1)
                st.switch_page('pages/Query.py')

            except mysql.connector.Error as e:
                st.error(f"Failed to connect to the database: {e}")
if __name__ == "__main__":
    main()