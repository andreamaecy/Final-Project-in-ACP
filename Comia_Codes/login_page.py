from tkinter import *
from tkinter import messagebox
import Welcome_page
from db_config import create_connection
import select_page

def login_page():
    """Function to create the login page GUI."""
    global username_entry, password_entry, next_window
    next_window = Toplevel()
    next_window.title("Login")
    next_window.geometry("350x450+300+200")  # Adjusted size for login page
    next_window.configure(bg="#fff")
    next_window.resizable(False, False)

    # Frame with #D9D9D9 color for the background
    top_frame = Frame(next_window, bg="#A09F9F", width=300, height=200)
    top_frame.pack(fill="both", padx=10, pady=8)

    # Subheading "Todong Todo" with black text color
    subheading = Label(top_frame, text="Todong Todo", fg="black", bg="#A09F9F",
                       font=("Bricolage Grotesque", 18), width=30, height=2)
    subheading.pack(pady=0)  # Reduced padding for closer spacing

    # Heading "ToDo Na Notes!"
    heading = Label(top_frame, text="ToDo Na Notes!", fg="#2B777B", bg="#A09F9F",
                    font=("Bricolage Grotesque", 24, "bold"))
    heading.pack(pady=1)  # Reduced padding for closer spacing

    # Username and Password Labels and Entry boxes inside the top frame
    username_label = Label(top_frame, text="Username/Email", fg="#2B777B", bg="#A09F9F", font=("Bree Serif", 12))
    username_label.pack(pady=5)

    global username_entry
    username_entry = Entry(top_frame, width=26, font=("Bree Serif", 14))
    username_entry.pack(pady=5)

    password_label = Label(top_frame, text="Password", fg="#2B777B", bg="#A09F9F", font=("Bree Serif", 12))
    password_label.pack(pady=5)

    global password_entry
    password_entry = Entry(top_frame, width=26, font=("Bree Serif", 14), show="*")
    password_entry.pack(pady=5)

    # Curved Sign In Button using Canvas
    canvas = Canvas(top_frame, width=250, height=40, bg="#2B777B", bd=0, highlightthickness=0)
    canvas.pack(pady=20)

    # Create the button shape and add text
    
    canvas.create_text(125, 20, text="Sign In", font=("Montserrat", 14), fill="white")

    # Bind the canvas to handle click
    canvas.bind("<Button-1>", sign_in_action)
    

    # Now, the "WELCOME BACK" and "Ready" texts will be outside the top frame.
    welcome_label = Label(next_window, text="WELCOME BACK", fg="#2B777B", bg="#fff", font=("Mukta Vaani", 16))
    welcome_label.pack(pady=5)

    ready_label = Label(next_window, text="Ready for another note taking adventure?", fg="#2B777B", bg="#fff", font=("Moon Dance", 12))
    ready_label.pack(pady=10)

    next_window.mainloop()

def sign_in_action(event=None):
    """Handle the Sign In button click."""
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return
        
    conn = create_connection()
    if not conn:
        messagebox.showerror("Error", "Database connection failed")
        return
        
    try:
        cursor = conn.cursor()
        # Check if the user exists and password matches
        if '@' in username:
            cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (username, password))
        else:
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")
            next_window.destroy()  # Close login window
            select_page.set_current_user(user[0])  # Set current user ID
            select_page.select_page()  # Open select page
        else:
            messagebox.showerror("Error", "Invalid username/email or password")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        conn.close()
