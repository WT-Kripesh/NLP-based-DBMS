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
#from ttkbootstrap import Style
from NLP_module.Query_generator import get_query
import NLP_module.database_structure as database_structure
#from database_connection import cursor, connection, db_config
from NLP_module.database_connection import db_config



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#for centering the window
def center_window(window):
    global screen_width,screen_height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = int(screen_width * 0.60)  # 58.6% of screen width
    window_height = int(screen_height * 0.725)  # 71.5% of screen height

    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

#for selecting database at the beginning
def select_database(selected_db, root):
    if selected_db:
        #close the selection window and open the main application window
        root.destroy()
        app_window = ctk.CTk()
        open_main_application(selected_db, app_window)
    else:
        messagebox.showwarning("No Database Selected", "Please select a database")


def open_main_application(selected_db, app_window):

    # Set up the main application window (ttkbootstrap styling used)
    #style = Style(theme='flatly')
    #root = style.master

    app_window.title("NLP-Based DBMS")
    #adjust the window size
    #app_window.geometry("800x550")
    window_width = 1080
    window_height = 800

    #centre the window
    center_window(app_window)

    db_config['database'] = selected_db

    #toggle light/dark mode
    def changeMode():
        val = switch.get()
        if val:
            ctk.set_appearance_mode("light")

        else:
            ctk.set_appearance_mode("dark")

    def execute_query(event=None):
        NL_query = query_entry.get()
        #using function from engine 
        #query generated from engine will be stored in this variable
        sql_query = get_query(NL_query, cursor)       

        try:
            #execute query
            cursor.execute(sql_query)
            #fetch results
            results = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description]

            # Display results in the text widget
            result_text.delete(1.0, tk.END)
            table = tabulate(results, headers=column_names, tablefmt='simple')
            result_text.insert(tk.END, "SQL Query\n")
            result_text.insert(tk.END, sql_query)
            result_text.insert(tk.END, "\n\n")
        
            result_text.insert(tk.END, table)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


    #function to display tables when the app starts
    def display_tables():
        #clear the result_text widget first
        tables_text.delete(1.0, tk.END)

        #fetch the tables from the database
        tables = database_structure.find_all_the_tables_in_a_database(db_config['database'],cursor)

        #insert the list of tables into the result_text widget
        for table in tables:
            attributes = database_structure.find_all_the_columns_in_a_table_from_given_database_with_datatype(db_config['database'],table,cursor)
            # print(attributes)
            final_table_content = ''
            for index , attribute in enumerate(attributes):
                temp_key = list(attribute.keys())[0]
                temp_value = list(attribute.values())[0]
                temp = temp_key + ' : ' + temp_value  
                if index != len(attributes) - 1:
                    final_table_content +=  temp + '  |  '
                else:
                    final_table_content +=  temp


            tables_text.insert(tk.END,f"# {table} -> {final_table_content}\n")


    # Create and place widgets

    #light/dark mode toggle switch
    switch = ctk.CTkSwitch(app_window, text="Light Mode", onvalue=1,offvalue=0,command=changeMode)
    switch.pack(anchor="e",padx=10, pady=0)

    #for displaying tables on startup
    label_tables = ctk.CTkLabel(app_window, text=f"Tables in Database '{db_config['database']}':", font=("arial",16))
    label_tables.pack(padx=30,pady=5)

    tables_text = ctk.CTkTextbox(app_window,width=int(screen_width*0.516),height=90, wrap='word', font=("Courier",16),corner_radius=6)
    tables_text.pack(padx=30, pady=8)

    label_query = ctk.CTkLabel(app_window, text="Enter Natural Language Query:", font=("arial",18))
    label_query.pack(padx=30,pady=8)

    query_entry = ctk.CTkEntry(app_window,width=int(screen_width*0.516),height=30,font=("arial",16), corner_radius=6, placeholder_text="eg: show all of the items")
    query_entry.pack(padx=30, pady=5)
    query_entry.bind("<Return>", execute_query)

    execute_button = ctk.CTkButton(app_window, text="Execute Query", command=execute_query, font=("abcg",16,"bold"))
    execute_button.pack(pady=10)

    result_text = ctk.CTkTextbox(app_window,width=int(screen_width*0.516),height=400, wrap='word', font=("Courier",15),corner_radius=6, border_width=1, border_color="#F0E68C" )
    
    result_text.pack(padx=30, pady=(4,15))



    #display tables on startup
    display_tables()

    #start the mainloop for app window
    app_window.mainloop()

    #close the cursor and connection
    cursor.close()
    connection.close()

def start_database_selection(db_config, db_select_root):
    db_select_root.title("NLP based DMBS")
    #root.geometry("800x550")

    window_width = 800
    window_height = 550

    #centre the window
    center_window(db_select_root)

    #fetch the local databases
    databases = database_structure.find_all_databases(cursor)

    def changeMode():
        val = switch.get()
        if val:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    #light/dark mode toggle switch
    switch = ctk.CTkSwitch(db_select_root, text="Light Mode", onvalue=1,offvalue=0,command=changeMode)
    switch.pack(anchor="e",padx=10, pady=0)

    #creating frame for containing components
    frame = ctk.CTkFrame(master=db_select_root,border_width=1,border_color="#F7F2C4")
    frame.pack(expand=True)

    #dropdown menu for database selection
    selected_db = tk.StringVar(db_select_root)
    database_label = ctk.CTkLabel(master=frame, text="Select Database", font=("arial",20))
    database_label.pack(padx=20,pady=10)

    database_menu = ctk.CTkComboBox(master=frame, width=int(screen_width*0.219), height=30,values=databases,dropdown_font=("arial",15),
                                    variable=selected_db, font=("arial",15))
    database_menu.pack(padx=20,pady=10)

    #button to proceed with the selected database
    proceed_button = ctk.CTkButton(master=frame, text="Proceed",font=("arial",15), command=lambda: 
                               select_database(selected_db.get(), db_select_root))
    proceed_button.pack(pady=20)

    #start the selection window
    db_select_root.mainloop()


####

#for login page from here onwards

def login():
    login_root = ctk.CTk()
    login_root.title("NLP based DMBS")

    window_width = 800
    window_height = 550

    #centre the window
    center_window(login_root)

    def update_db_config():
        db_config['host'] = host_entry.get()
        db_config['user'] = user_entry.get()
        db_config['password'] = password_entry.get()
        return

    def changeMode():
        val = switch.get()
        if val:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    #light/dark mode toggle switch
    switch = ctk.CTkSwitch(login_root, text="Light Mode", onvalue=1,offvalue=0,command=changeMode)
    switch.pack(anchor="e",padx=10, pady=0)

    #creating frame for containing components
    frame = ctk.CTkFrame(master=login_root,border_width=1,border_color="#F7F2C4")
    frame.pack(expand=True)

    database_label = ctk.CTkLabel(master=frame, text="MySQL authentication", font=("arial",18))
    database_label.pack(padx=20,pady=10)

    #series of entries to gather credentials
    
    label_host = ctk.CTkLabel(frame, text="Host:", font=("arial",14))
    label_host.pack(anchor="w",padx=30,pady=1)
    host_entry = ctk.CTkEntry(frame,width=int(screen_width*0.219),height=30,font=("arial",14), corner_radius=6, placeholder_text="localhost")
    host_entry.pack(padx=30)
    #pre-set the default value
    host_entry.insert(0, "localhost")

    label_user = ctk.CTkLabel(frame, text="User:", font=("arial",14))
    label_user.pack(anchor="w",padx=30,pady=1)
    user_entry = ctk.CTkEntry(frame,width=int(screen_width*0.219),height=30,font=("arial",14), corner_radius=6, placeholder_text="root")
    user_entry.pack(padx=30)
    #pre-set the defualt value
    user_entry.insert(0, "root")
    
    label_password = ctk.CTkLabel(frame, text="Password:", font=("arial",14))
    label_password.pack(anchor="w",padx=30,pady=1)
    password_entry = ctk.CTkEntry(frame,width=int(screen_width*0.219),height=30,font=("arial",14), corner_radius=6, placeholder_text="hum_vinod", show="•")
    password_entry.pack(padx=30)
    password_entry.bind("<Return>",lambda event: authenticate(login_root,update_db_config()))

    #button to proceed with the selected database
    proceed_button = ctk.CTkButton(master=frame, text="Proceed",font=("arial",15), command=lambda: 
                               authenticate(login_root,update_db_config()))
    proceed_button.pack(pady=20)

    #start the selection window
    login_root.mainloop()



def authenticate(login_root,dummy,event=None):
    if db_config:
        print(db_config)
        
        try:
            login_root.destroy()

            global cursor,connection
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            db_select_root = ctk.CTk()
            start_database_selection(db_config, db_select_root)
        
        except:
            messagebox.showwarning("Authentication failed", "Please check credentials")
   
    else:
        messagebox.showwarning("Authentication failed", "Please check credentials")

#run the application with login window.
login()
