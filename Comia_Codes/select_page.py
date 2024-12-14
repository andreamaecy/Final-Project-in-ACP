from tkinter import *
from tkinter import ttk, messagebox, filedialog
import note_taking
import view_notes
from db_config import create_connection
import os

current_user_id = None

def set_current_user(user_id):
    global current_user_id
    current_user_id = user_id

def select_page():
    select_window = Tk()
    select_window.title("Select Page")
    select_window.geometry("1000x600+300+200")
    select_window.configure(bg="#2B777B")
    select_window.resizable(False, False)

    # Center frame
    center_frame = Frame(select_window, bg="#2B777B")
    center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Title
    Label(center_frame, text="Choose Your Action",
          font=("Microsoft Yahei UI Light", 25, "bold"),
          fg="white", bg="#2B777B").pack(pady=(0, 40))

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox',
                   fieldbackground='white',
                   background='white',
                   foreground='black')

    # Year selection
    Label(center_frame, text="Year Level:",
          font=("Microsoft Yahei UI Light", 12),
          fg="white", bg="#2B777B").pack()

    year_var = StringVar()
    year_combo = ttk.Combobox(center_frame,
                             textvariable=year_var,
                             values=["1st Year", "2nd Year", "3rd Year", "4th Year"],
                             state="readonly",
                             width=30)
    year_combo.pack(pady=(5, 20))

    # Semester selection
    Label(center_frame, text="Semester:",
          font=("Microsoft Yahei UI Light", 12),
          fg="white", bg="#2B777B").pack()

    sem_var = StringVar()
    sem_combo = ttk.Combobox(center_frame,
                            textvariable=sem_var,
                            state="readonly",
                            width=30)
    sem_combo.pack(pady=(5, 20))

    def update_semester(*args):
        year = year_combo.get()
        if year in ["1st Year", "2nd Year"]:
            sem_combo['values'] = ["1st Semester", "2nd Semester"]
        elif year in ["3rd Year", "4th Year"]:
            sem_combo['values'] = ["1st Semester", "2nd Semester", "Summer Class"]
        sem_combo.set('')

    # Bind the update function to the year combobox
    year_combo.bind('<<ComboboxSelected>>', update_semester)

    # Save location
    Label(center_frame, text="Save Location:",
          font=("Microsoft Yahei UI Light", 12),
          fg="white", bg="#2B777B").pack()

    # Frame for entry and button
    save_frame = Frame(center_frame, bg="#2B777B")
    save_frame.pack(pady=(5, 20))

    save_var = StringVar(value=os.path.join(os.path.dirname(__file__), "notes"))
    save_entry = Entry(save_frame, textvariable=save_var, width=50)
    save_entry.pack(side=LEFT, padx=(0, 10))

    def browse_location():
        dir_path = filedialog.askdirectory(initialdir=save_var.get())
        if dir_path:
            save_var.set(dir_path)

    Button(save_frame, text="Browse",
           command=browse_location,
           bg="#1F5C5E", fg="white",
           font=("Microsoft Yahei UI Light", 10)).pack(side=LEFT)

    # Button frame
    button_frame = Frame(center_frame, bg="#2B777B")
    button_frame.pack(pady=(20, 0))

    def on_enter(e):
        e.widget['background'] = '#164445'

    def on_leave(e):
        e.widget['background'] = '#1F5C5E'

    def validate_and_create():
        year = year_combo.get()  # Get directly from combobox instead of StringVar
        if not year:
            messagebox.showerror("Error", "Please select a Year Level")
            return

        semester = sem_combo.get()  # Get directly from combobox instead of StringVar
        if not semester:
            messagebox.showerror("Error", "Please select a Semester")
            return

        save_location = save_var.get()
        try:
            os.makedirs(save_location, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create save location: {str(e)}")
            return

        save_preferences(year, semester, save_location)
        select_window.destroy()
        note_taking.note_taking_page(year, semester, save_location)

    def validate_and_view():
        year = year_combo.get()  # Get directly from combobox instead of StringVar
        if not year:
            messagebox.showerror("Error", "Please select a Year Level")
            return

        semester = sem_combo.get()  # Get directly from combobox instead of StringVar
        if not semester:
            messagebox.showerror("Error", "Please select a Semester")
            return

        save_location = save_var.get()
        save_preferences(year, semester, save_location)
        select_window.destroy()
        view_notes.view_notes_page(year, semester, save_location)

    # Create Note button
    create_btn = Button(button_frame,
                       text="Create Note",
                       command=validate_and_create,
                       font=("Microsoft Yahei UI Light", 12),
                       fg="white",
                       bg="#1F5C5E",
                       width=20,
                       height=2,
                       cursor="hand2")
    create_btn.pack(side=LEFT, padx=10)
    create_btn.bind("<Enter>", on_enter)
    create_btn.bind("<Leave>", on_leave)

    # View Notes button
    view_btn = Button(button_frame,
                     text="View Notes",
                     command=validate_and_view,
                     font=("Microsoft Yahei UI Light", 12),
                     fg="white",
                     bg="#1F5C5E",
                     width=20,
                     height=2,
                     cursor="hand2")
    view_btn.pack(side=LEFT, padx=10)
    view_btn.bind("<Enter>", on_enter)
    view_btn.bind("<Leave>", on_leave)

    # Load saved preferences
    if current_user_id:
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT year, semester, save_location 
                    FROM user_preferences
                    WHERE user_id = ?
                """, (current_user_id,))
                prefs = cursor.fetchone()
                if prefs:
                    year, semester, save_location = prefs
                    year_combo.set(year)
                    # This will trigger the update_semester function
                    update_semester()
                    sem_combo.set(semester)
                    save_var.set(save_location)
            except Exception as e:
                print(f"Error loading preferences: {e}")
            finally:
                conn.close()

    select_window.mainloop()

def save_preferences(year, semester, save_location):
    if not current_user_id:
        return

    conn = create_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences 
            (user_id, year, semester, save_location)
            VALUES (?, ?, ?, ?)
        """, (current_user_id, year, semester, save_location))
        conn.commit()
    except Exception as e:
        print(f"Error saving preferences: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    select_page()
