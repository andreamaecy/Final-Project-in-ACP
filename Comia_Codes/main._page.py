from tkinter import *
from tkinter import messagebox
import login_page 
import Welcome_page 
from db_config import create_connection
import re

def main_page():
    """Function to create the main page GUI."""
    global root, user, user_1
    root = Tk()
    root.title("Create Account")
    root.geometry("1000x600+300+200")
    root.configure(bg="#fff")
    root.resizable(False, False)

    img = PhotoImage(file="Logo.png")
    Label(root, image=img, bg="white").place(x=600, y=50)

    frame = Frame(root, width=622, height=600, bg="#2B777B")
    frame.place(x=0, y=0)

    # Welcome heading
    heading = Label(frame, text="Welcome to ToDo \n Na Notes!", fg="white", bg="#2B777B",
                    font=("Bricolage Grotesque", 40, "bold"))
    heading.place(relx=0.5, rely=0.20, anchor="center") 

    # Subheading below the welcome message
    heading_2 = Label(frame, text="Your Notes are waiting for you.", fg="white", bg="#2B777B",
                      font=("Bricolage Grotesque", 20))
    heading_2.place(relx=0.5, rely=0.32, anchor="center") 

    # Username/Email label
    heading_3 = Label(frame, text="Username/Email", fg="white", bg="#2B777B", font=("Bree Serif", 16))
    heading_3.place(x=60, y=250)  

    # Entry for Username/Email 
    user = Entry(frame, width=40, fg="#363636", border=0, bg="#D9D9D9", font=("Bree Serif", 16))
    user.place(x=60, y=280)  
    user.config(highlightthickness=1, highlightbackground="#ccc", highlightcolor="#888")

    # Password label
    heading_4 = Label(frame, text="Password", fg="white", bg="#2B777B", font=("Bree Serif", 16))
    heading_4.place(x=60, y=330)

    # Entry for Password
    user_1 = Entry(frame, width=40, fg="#363636", border=0, bg="#D9D9D9", font=("Bree Serif", 16), show="*")
    user_1.place(x=60, y=360)  
    user_1.config(highlightthickness=1, highlightbackground="#ccc", highlightcolor="#888")

    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def create_account():
        """Handle account creation."""
        username_email = user.get()
        password = user_1.get()
        
        if not username_email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Determine if input is email or username
        is_email = '@' in username_email
        
        # Validate email format if it's an email
        if is_email and not validate_email(username_email):
            messagebox.showerror("Error", "Invalid email format")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        conn = create_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed")
            return
            
        try:
            cursor = conn.cursor()
            
            # Check if username/email already exists
            if is_email:
                cursor.execute("SELECT id FROM users WHERE email = ?", (username_email,))
            else:
                cursor.execute("SELECT id FROM users WHERE username = ?", (username_email,))
                
            if cursor.fetchone():
                messagebox.showerror("Error", "Username/Email already exists")
                return
                
            # Create new user
            if is_email:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username_email.split('@')[0], username_email, password)
                )
            else:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username_email, f"{username_email}@todonotes.com", password)
                )
                
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            root.destroy()
            login_page.login_page()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    # Create Account Button
    canvas = Canvas(frame, width=200, height=50, bg="#2B777B", bd=0, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.75, anchor="center")

    canvas.create_rounded_rectangle(0, 0, 200, 50, radius=25, fill="#CAC5C5", outline="")

    canvas.create_text(100, 25, text="Create an Account", font=("Montserrat", 14), fill="black")
    
    # Bind the create account button to the create_account function
    canvas.bind("<Button-1>", lambda event: create_account())

    have_account_label = Label(frame, text="Have an Account?", fg="white", bg="#2B777B", font=("Bree Serif", 14))
    have_account_label.place(relx=0.5, rely=0.83, anchor="center") 

    sign_in_text = Label(frame, text="Sign In", fg="#040548", bg="#2B777B", font=("Bree Serif", 14, "underline"))
    sign_in_text.place(relx=0.5, rely=0.88, anchor="center") 
    sign_in_text.bind("<Button-1>", lambda event: login_page.login_page()) 

    root.mainloop()

def open_next_page(event=None):
    """Open the login page (second GUI)."""
    login_page.login_page()  # Call the login page function from the imported module

# Create a helper function to draw rounded rectangles
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    """
    Creates a rounded rectangle using the Canvas widget.
    The coordinates (x1, y1) are the top-left corner, and (x2, y2) are the bottom-right corner.
    """
    self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, **kwargs)
    self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, **kwargs)
    self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, **kwargs)
    self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, **kwargs)
    self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
    self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)

# Attach the helper function to the Canvas widget
Canvas.create_rounded_rectangle = create_rounded_rectangle

# Start the application with the main page
main_page()
