#Import libraries
from tkinter import *
from tkinter import messagebox
import psycopg2

#Define constants
WIDTH, HEIGHT = 670, 450

#Visual stuff (frames and widgets)
def title_frame(root):
    title_frame = Frame(root)
    title_frame.pack(fill='both')
    return title_frame

def main_frame(root):
    main_frame = Frame(root, bg='white')
    main_frame.pack(fill='both')
    return main_frame

def draw_title(titleFrame):
    title = Label(titleFrame, text='Patients data', font='Arial 24', pady=10)
    title.pack()
    return title

def draw_labels(mainFrame):
    dni_label = Label(mainFrame, text='DNI: ', font='Arial 18', pady=10, padx=5, bg='white')
    dni_label.grid(row=0, sticky='e')
    full_name_label = Label(mainFrame, text='Full name: ', font='Arial 18', pady=10, padx=5, bg='white')
    full_name_label.grid(row=1, sticky='e')
    osde_label = Label(mainFrame, text='OSDE: ', font='Arial 18', pady=10, padx=5, bg='white')
    osde_label.grid(row=2, sticky='e')
    money_label = Label(mainFrame, text='Paid per month: ', font='Arial 18', pady=10, padx=5, bg='white')
    money_label.grid(row=3, sticky='e')

def dni_entry(mainFrame):
    dni_entry = Entry(mainFrame, font='Arial 18')
    dni_entry.grid(row=0, column=1)
    return dni_entry

def full_name_entry(mainFrame):
    full_name_entry = Entry(mainFrame, font='Arial 18')
    full_name_entry.grid(row=1, column=1)
    return full_name_entry

def osde_radiobuttons(mainFrame):
    osde_value = IntVar(value=1)
    osde_radiobutton_yes = Radiobutton(mainFrame, text='Yes', variable=osde_value, value=1, font='Arial 18', bg='white')
    osde_radiobutton_yes.grid(row=2, column=1, sticky='w')
    osde_radiobutton_no = Radiobutton(mainFrame, text='No', variable=osde_value, value=0, font='Arial 18', bg='white')
    osde_radiobutton_no.grid(row=2, column=1, sticky='e')
    return osde_value

def money_paid_entry(mainFrame):
    money_paid_entry = Entry(mainFrame, font='Arial 18')
    money_paid_entry.grid(row=3, column=1)
    return money_paid_entry

def button_frame(root):
    button_frame = Frame(root, bg='white')
    button_frame.pack(fill='both')
    return button_frame

def add_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection):
    add_patient_button = Button(buttonFrame, text='Add patient', font='Arial 12', pady=10, padx=10, command=lambda:add_patient(dni, fullName, osde, moneyPaid, connection))
    add_patient_button.grid(row=0, column=0, padx=20, pady=30)

def search_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection):
    search_patient_button = Button(buttonFrame, text='Search patient', font='Arial 12', pady=10, padx=10, command=lambda:search_patient(dni, fullName, osde, moneyPaid, connection))
    search_patient_button.grid(row=0, column=1, padx=20, pady=30)

def modify_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection):
    modify_patient_button = Button(buttonFrame, text='Modify patient', font='Arial 12', pady=10, padx=10, command=lambda:modify_patient(dni, fullName, osde, moneyPaid, connection))
    modify_patient_button.grid(row=0, column=2, padx=20, pady=30)

def delete_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection):
    delete_patient_button = Button(buttonFrame, text='Delete patient', font='Arial 12', pady=10, padx=10, command=lambda:delete_patient(dni, fullName, osde, moneyPaid, connection))
    delete_patient_button.grid(row=0, column=3, padx=20, pady=30)

def clear_button(buttonFrame, dni, fullName, osde, moneyPaid):
    clear_button = Button(buttonFrame, text='Clear fields', font='Arial 12', pady=10, padx=10, command=lambda:clear_fields(dni, fullName, osde, moneyPaid))
    clear_button.grid(row=1, column=1, columnspan=2, sticky='e')

def export_data_button(buttonFrame, connection):
    clear_button = Button(buttonFrame, text='Export data', font='Arial 12', pady=10, padx=10, command=lambda:export_data(connection))
    clear_button.grid(row=1, column=1, columnspan=2, sticky='w')

#Button commands (SQL commands)
def add_patient(dni, fullName, osde, moneyPaid, connection):
    dni_value = dni.get()
    full_name_value = fullName.get()
    osde_value = True if osde.get() == 1 else False
    money_paid_value = moneyPaid.get()
    if dni_value != '' and full_name_value != '' and money_paid_value != 0:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO patients_data (dni, full_name, osde, paid_per_month) VALUES (%s, %s, %s, %s);", 
                        (dni_value, full_name_value, osde_value, money_paid_value))
            cursor.close()
            messagebox.showinfo('Information', 'Data saved successfully')
        except Exception as ex:
            messagebox.showerror('Error', ex)
        dni.delete(0, 'end')
        fullName.delete(0, 'end')
        osde.set(1)
        moneyPaid.delete(0, 'end')
    else:
        messagebox.showwarning('Warning', 'Please fill in the fields with the appropriate information')

def search_patient(dni, fullName, osde, moneyPaid, connection):
    dni_value = dni.get()
    full_name_value = fullName.get()
    if dni_value != '':
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM patients_data WHERE dni=%s;", (dni_value,))
            patient = cursor.fetchone()
            dni_value = patient[0]
            full_name_value = patient[1]
            osde_value = patient[2]
            money_paid_value = patient[3]
            dni.delete(0, 'end')
            fullName.delete(0, 'end')
            osde.set(1)
            moneyPaid.delete(0, 'end')
            dni.insert(INSERT, dni_value)
            fullName.insert(INSERT, full_name_value)
            osde.set(1 if osde_value else 0)
            moneyPaid.insert(INSERT, money_paid_value)
            cursor.close()
        except Exception as ex:
            messagebox.showerror('Error', ex)
    elif full_name_value != '':
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM patients_data WHERE full_name=%s;", (full_name_value,))
            patient = cursor.fetchone()
            dni_value = patient[0]
            full_name_value = patient[1]
            osde_value = patient[2]
            money_paid_value = patient[3]
            dni.delete(0, 'end')
            fullName.delete(0, 'end')
            osde.set(1)
            moneyPaid.delete(0, 'end')
            dni.insert(INSERT, dni_value)
            fullName.insert(INSERT, full_name_value)
            osde.set(1 if osde_value else 0)
            moneyPaid.insert(INSERT, money_paid_value)
            cursor.close()
        except Exception as ex:
            messagebox.showerror('Error', ex)
    else:
        messagebox.showwarning('Warning', 'Please fill in the dni field or the full name field to carry out the search')

def modify_patient(dni, fullName, osde, moneyPaid, connection):
    dni_value = dni.get()
    full_name_value = fullName.get()
    osde_value = True if osde.get() == 1 else False
    money_paid_value = moneyPaid.get()
    if dni_value != '' and full_name_value != '' and money_paid_value != '':
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE patients_data SET dni=%s, full_name=%s, osde=%s, paid_per_month=%s WHERE dni=%s", (dni_value, full_name_value, osde_value, money_paid_value, dni_value))
            cursor.close()
            messagebox.showinfo('Information', 'Data modified successfully')
        except Exception as ex:
            messagebox.showerror('Error', ex)
    else:
        messagebox.showwarning('Warning', 'Please do a search to be able to modify a patients data')
    dni.delete(0, 'end')
    fullName.delete(0, 'end')
    osde.set(1)
    moneyPaid.delete(0, 'end')

def delete_patient(dni, fullName, osde, moneyPaid, connection):
    dni_value = dni.get()
    full_name_value = fullName.get()
    if dni_value != '':
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM patients_data WHERE dni=%s;", (dni_value,))
            cursor.close()
            messagebox.showinfo('Information', 'Data deleted successfully')
        except Exception as ex:
            messagebox.showerror('Error', ex)
    elif full_name_value != '':
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM patients_data WHERE fullName=%s;", (full_name_value,))
            cursor.close()
            messagebox.showinfo('Information', 'Data deleted successfully')
        except Exception as ex:
            messagebox.showerror('Error', ex)
    else:
        messagebox.showwarning('Warning', 'Please fill in the dni field or the full name field to carry out the search')
    dni.delete(0, 'end')
    fullName.delete(0, 'end')
    osde.set(1)
    moneyPaid.delete(0, 'end')

def clear_fields(dni, fullName, osde, moneyPaid):
    dni.delete(0, 'end')
    fullName.delete(0, 'end')
    osde.set(1)
    moneyPaid.delete(0, 'end')

def export_data(connection):
    sql_command = "COPY patients_data TO STDOUT WITH CSV DELIMITER ';';"
    route = 'C:/Users/maspi/OneDrive/Documentos/patients_data/patients_data.csv'
    try:
        cursor = connection.cursor()
        with open(route, 'w') as file:
            cursor.copy_expert(sql_command, file)
        cursor.close()
        messagebox.showinfo('Information', f'Data exported successfully to {route}')
    except Exception as ex:
        print(ex)
        messagebox.showerror('Error', ex)

#Database connection and disconnection
def database_connection():
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = 'ladradorcriollo718',
            database = 'patients',
            port='5432'
        )
        print('Successful connection to database')
    except Exception as ex:
        print(ex)
    return connection

def database_disconnection(connection):
    try:
        connection.close()
        print('Successful disconnection to database')
    except Exception as ex:
        print(ex)

#Main function
def main():
    #Database connection and define cursor to execute sql requests
    connection = database_connection()
    connection.autocommit = True

    #Make the root
    root = Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.config(bg='white')
    root.resizable(False, False)
    root.title('Patient Data Administrator')

    #Split the screen in frames
    titleFrame = title_frame(root)
    mainFrame = main_frame(root)
    buttonFrame = button_frame(root)

    #Draw widgets and pass arguments to them so thy can execute comands and modify the screen
    draw_title(titleFrame)
    draw_labels(mainFrame)
    dni = dni_entry(mainFrame)
    fullName = full_name_entry(mainFrame)
    osde = osde_radiobuttons(mainFrame)
    moneyPaid = money_paid_entry(mainFrame)
    add_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection)
    search_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection)
    modify_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection)
    delete_patient_button(buttonFrame, dni, fullName, osde, moneyPaid, connection)
    clear_button(buttonFrame, dni, fullName, osde, moneyPaid)
    export_data_button(buttonFrame, connection)

    #Window mainloop
    root.mainloop()

    #Database disconnection
    database_disconnection(connection)

#Run program
if __name__ == '__main__':
    main()