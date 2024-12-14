from tkinter import *
from PIL import Image, ImageTk
import select_page

def Welcome_page():
    """Function to create the welcome page GUI."""
    next_window_1 = Toplevel()
    next_window_1.title("Welcome To ToDo Na Notes!")
    next_window_1.geometry("1000x600")
    next_window_1.configure(bg="#fff")
    next_window_1.resizable(False, False)

    try:
        original_image = Image.open("Welcome.png")
        resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)

        image = ImageTk.PhotoImage(resized_image)
        next_window_1.image = image  # Prevent garbage collection
       
        label = Label(next_window_1, image=image)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        canvas = Canvas(next_window_1, width=100, height=100, bg="#fff", highlightthickness=0)
        canvas.place(relx=0.73, rely=0.82, anchor="center")  
        
        canvas.create_oval(10, 10, 90, 90, fill="#A09F9F", outline="") 
        canvas.create_text(50, 50, text="START", font=("Montserrat", 14, "bold"), fill="white")

        # Bind the canvas to handle click without passing any argument
        canvas.bind("<Button-1>", lambda event: select_page.select_page())  # No argument needed here

    except FileNotFoundError:
        print("Error: Image file not found. Check the file path!")
    except Exception as e:
        print(f"An error occurred: {e}")

    next_window_1.mainloop()
    
    
