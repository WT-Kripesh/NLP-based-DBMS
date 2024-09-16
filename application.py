#build a GUI for our application using tkinter
#tkinter comes pre installed along with python
#pip install ttkbootstrap
#install tabulate if necessary
import sys
sys.path.insert(0, './NLP_module')

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tabulate import tabulate
from ttkbootstrap import Style
from engine import get_query             # type: ignore
#import database_structure
#from termcolor import colored

# Database configuration with credentials  :   change it if necessary
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'avot',                         
    'database': 'nlpdemo'
}

# Establish database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def execute_query():
    NL_query = query_entry.get()
    #using function from engine 
    #query generated from engine will be stored in this variable
    sql_query = get_query(NL_query)       

    try:
        #execute query
        cursor.execute(sql_query)
        #fetch results
        results = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        
        #close the cursor and connection
        cursor.close()
        conn.close()

        # Display results in the text widget, but first clearing it
        result_text.delete(1.0, tk.END)
        table = tabulate(results, headers=column_names, tablefmt='simple')
        result_text.insert(tk.END, table)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


# this is temporary. need to sort out file structure soon
def find_all_the_tables_in_a_database(database_name):
    cursor.execute(f"USE {database_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    return tables

#function to display tables when the app starts
def display_tables():
    #clear the result_text widget first
    result_text.delete(1.0, tk.END)

    #fetch the tables from the database
    tables = find_all_the_tables_in_a_database(db_config['database'])

    #insert the list of tables into the result_text widget
    for table in tables:
        result_text.insert(tk.END,f"- {table}\n")


# Set up the main application window (ttkbootstrap styling used)
style = Style(theme='flatly')
root = style.master
root.title("NLP-Based DBMS")

#adjust the window size
root.geometry("800x550")



# Create and place widgets
label = tk.Label(root, text="Enter Natural Language Query:", font=("Helvetica",14))
label.pack(anchor='w',padx=30,pady=10)

query_entry = tk.Entry(root, width=70, font=("Helvetica",12))
query_entry.pack(anchor='w', padx=30, pady=5)

execute_button = tk.Button(root, text="Execute Query", command=execute_query,
                           bg="#337ab7", fg="white", font=("Helvetica",12,"bold"))
execute_button.pack(pady=20)

result_text = tk.Text(root, wrap=tk.WORD, width=90, height=20, font=("Courier",10), bg="#f8f9fa")
result_text.pack(anchor='w', padx=30, pady=10)

#display tables on startup
display_tables()

# Run the application
root.mainloop()
