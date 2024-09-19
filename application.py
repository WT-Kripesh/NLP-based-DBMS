#build a GUI for our application using tkinter
#tkinter comes pre installed along with python
#customtkinter does NOT come pre installed 
#pip install customtkinter
#pip install ttkbootstrap
#install tabulate if necessary
import sys
sys.path.insert(0, './NLP_module')

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox,ttk 
import mysql.connector
from tabulate import tabulate
from ttkbootstrap import Style
from engine import get_query             # type: ignore
import database_structure_temp
from database_connection import cursor, connection, db_config

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#for selecting database at the beginning
def select_database(selected_db, root, app_window):
    if selected_db:
        #close the selection window and open the main application window
        root.destroy()
        open_main_application(selected_db, app_window)
    else:
        messagebox.showwarning("No Database Selected", "Please select a database")


def open_main_application(selected_db, app_window):

    # Set up the main application window (ttkbootstrap styling used)
    #style = Style(theme='flatly')
    #root = style.master

    app_window.title("NLP-Based DBMS")
    #adjust the window size
    app_window.geometry("800x550")

    db_config['database'] = selected_db

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
            connection.close()

            # Display results in the text widget
            result_text.delete(1.0, tk.END)
            table = tabulate(results, headers=column_names, tablefmt='simple')
            result_text.insert(tk.END, table)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


    #function to display tables when the app starts
    def display_tables():
        #clear the result_text widget first
        tables_text.delete(1.0, tk.END)

        #fetch the tables from the database
        tables = database_structure_temp.find_all_the_tables_in_a_database(db_config['database'],cursor)

        #insert the list of tables into the result_text widget
        for table in tables:
            attributes = database_structure_temp.find_all_the_columns_in_a_table_from_given_database(db_config['database'],table,cursor)
            temp = ', '.join(attributes)
            tables_text.insert(tk.END,f"# {table} : {temp}\n")


    # Create and place widgets

    #for displaying tables on startup
    label_tables = ctk.CTkLabel(app_window, text=f"Tables in Database '{db_config['database']}':", font=("arial",16))
    label_tables.pack(padx=30,pady=5)

    tables_text = ctk.CTkTextbox(app_window,width=700,height=80, wrap='word', font=("Courier",14),corner_radius=6)
    tables_text.pack(padx=30, pady=8)

    label_query = ctk.CTkLabel(app_window, text="Enter Natural Language Query:", font=("arial",16))
    label_query.pack(padx=30,pady=8)

    query_entry = ctk.CTkEntry(app_window,width=700,height=25,font=("arial",14), corner_radius=6, placeholder_text="eg: show all of the items")
    query_entry.pack(padx=30, pady=5)

    execute_button = ctk.CTkButton(app_window, text="Execute Query", command=execute_query, font=("abcg",16,"bold"))
    execute_button.pack(pady=10)

    result_text = ctk.CTkTextbox(app_window,width=700,height=300, wrap='word', font=("Courier",14),corner_radius=6, border_width=1, border_color="#F0E68C" )
    result_text.pack(padx=30, pady=8)



    #display tables on startup
    display_tables()

    #start the mainloop for app window
    app_window.mainloop()

def start_database_selection():
    root = ctk.CTk()
    root.title("NLP based DMBS")
    root.geometry("800x550")

    #fetch the local databases
    databases = database_structure_temp.find_all_databases(cursor)

    #creating frame for containing components
    frame = ctk.CTkFrame(master=root,border_width=1,border_color="#F7F2C4")
    frame.pack(expand=True)

    #dropdown menu for database selection
    selected_db = tk.StringVar(root)
    database_label = ctk.CTkLabel(master=frame, text="Select Database", font=("arial",20))
    database_label.pack(padx=20,pady=10)

    database_menu = ctk.CTkComboBox(master=frame, width=300, height=30,values=databases,dropdown_font=("arial",15),
                                    variable=selected_db, font=("arial",15))
    database_menu.pack(padx=20,pady=10)

    #button to proceed with the selected database
    proceed_button = ctk.CTkButton(master=frame, text="Proceed",font=("arial",15), command=lambda: 
                               select_database(selected_db.get(), root, app_window=ctk.CTk()))
    proceed_button.pack(pady=20)

    #start the selection window
    root.mainloop()

# Run the application with database selection window
start_database_selection()
