from tkinter import *
from tkinter import ttk, colorchooser, font, messagebox
from PIL import Image, ImageTk, ImageDraw
import os

class NoteTakingApp:
    def __init__(self, year, semester, save_location):
        self.root = Tk()
        self.root.title("Note Taking App")
        self.root.geometry("1200x700+100+50")
        self.root.configure(bg="#fff")
        self.root.resizable(True, True)

        # Initialize variables
        self.year = year
        self.semester = semester
        self.save_location = save_location
        self.current_color = "black"
        self.current_font = ("Arial", 12)
        self.drawing_enabled = False
        self.last_x = None
        self.last_y = None
        
        # Create main containers
        self.create_sidebar()
        self.create_main_area()
        
    def create_sidebar(self):
        """Create expandable sidebar with all tools"""
        # Sidebar frame
        self.sidebar = Frame(self.root, bg="#2B777B", width=200)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)
        
        # Style for the sidebar
        style = ttk.Style()
        style.configure("Tool.TButton", padding=5, width=20)
        
        # Expandable sections
        self.create_font_section()
        self.create_color_section()
        self.create_drawing_section()
        self.create_file_section()
        
    def create_font_section(self):
        """Create font customization section"""
        # Font frame
        font_frame = Frame(self.sidebar, bg="#2B777B")
        font_frame.pack(fill=X, padx=5, pady=5)
        
        # Font family
        Label(font_frame, text="Font:", bg="#2B777B", fg="white").pack(anchor=W)
        self.font_family = ttk.Combobox(font_frame, values=list(font.families()))
        self.font_family.set("Arial")
        self.font_family.pack(fill=X, padx=5, pady=2)
        self.font_family.bind("<<ComboboxSelected>>", self.change_font)
        
        # Font size
        Label(font_frame, text="Size:", bg="#2B777B", fg="white").pack(anchor=W)
        self.font_size = ttk.Combobox(font_frame, values=[str(i) for i in range(8, 73, 2)])
        self.font_size.set("12")
        self.font_size.pack(fill=X, padx=5, pady=2)
        self.font_size.bind("<<ComboboxSelected>>", self.change_font)
        
    def create_color_section(self):
        """Create color selection section"""
        color_frame = Frame(self.sidebar, bg="#2B777B")
        color_frame.pack(fill=X, padx=5, pady=5)
        
        Label(color_frame, text="Text Color:", bg="#2B777B", fg="white").pack(anchor=W)
        self.color_btn = Button(color_frame, text="Choose Color", 
                              command=self.choose_color,
                              bg="#1F5C5E", fg="white")
        self.color_btn.pack(fill=X, padx=5, pady=2)
        
    def create_drawing_section(self):
        """Create drawing tools section"""
        draw_frame = Frame(self.sidebar, bg="#2B777B")
        draw_frame.pack(fill=X, padx=5, pady=5)
        
        # Drawing mode toggle
        self.draw_btn = Button(draw_frame, text="Enable Drawing", 
                             command=self.toggle_drawing,
                             bg="#1F5C5E", fg="white")
        self.draw_btn.pack(fill=X, padx=5, pady=2)
        
        # Eraser
        self.eraser_btn = Button(draw_frame, text="Eraser", 
                               command=self.toggle_eraser,
                               bg="#1F5C5E", fg="white")
        self.eraser_btn.pack(fill=X, padx=5, pady=2)

        # Clear Canvas
        self.clear_btn = Button(draw_frame, text="Clear Canvas", 
                              command=self.clear_canvas,
                              bg="#1F5C5E", fg="white")
        self.clear_btn.pack(fill=X, padx=5, pady=2)
        
    def create_file_section(self):
        """Create file operations section"""
        file_frame = Frame(self.sidebar, bg="#2B777B")
        file_frame.pack(fill=X, padx=5, pady=5)
        
        # Save button
        self.save_btn = Button(file_frame, text="Save Note", 
                             command=self.save_note,
                             bg="#1F5C5E", fg="white")
        self.save_btn.pack(fill=X, padx=5, pady=2)
        
        # View Notes button
        self.view_btn = Button(file_frame, text="View Notes", 
                             command=self.view_notes,
                             bg="#1F5C5E", fg="white")
        self.view_btn.pack(fill=X, padx=5, pady=2)

    def create_main_area(self):
        """Create main note-taking area"""
        self.main_frame = Frame(self.root, bg="white")
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Create a PanedWindow to separate text and canvas
        self.paned = PanedWindow(self.main_frame, orient=VERTICAL)
        self.paned.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Text area frame
        text_frame = Frame(self.paned)
        self.paned.add(text_frame)
        
        # Text area with scrollbar
        self.text_area = Text(text_frame, wrap=WORD, font=self.current_font)
        scrollbar = Scrollbar(text_frame, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Canvas frame
        canvas_frame = Frame(self.paned)
        self.paned.add(canvas_frame)
        
        # Drawing canvas with scrollbar
        self.canvas = Canvas(canvas_frame, bg="white", height=200)
        canvas_scrollbar = Scrollbar(canvas_frame, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=canvas_scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        canvas_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
            
    def change_font(self, event=None):
        """Change text font"""
        family = self.font_family.get()
        size = int(self.font_size.get())
        self.current_font = (family, size)
        self.text_area.configure(font=self.current_font)
        
    def choose_color(self):
        """Open color picker"""
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.current_color = color
            self.text_area.configure(fg=color)
            
    def toggle_drawing(self):
        """Toggle drawing mode"""
        self.drawing_enabled = not self.drawing_enabled
        if self.drawing_enabled:
            self.draw_btn.configure(text="Disable Drawing", bg="#164445")
        else:
            self.draw_btn.configure(text="Enable Drawing", bg="#1F5C5E")
            
    def toggle_eraser(self):
        """Toggle eraser mode"""
        if self.current_color != "white":
            self.previous_color = self.current_color
            self.current_color = "white"
            self.eraser_btn.configure(bg="#164445")
        else:
            self.current_color = self.previous_color
            self.eraser_btn.configure(bg="#1F5C5E")

    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
            
    def start_drawing(self, event):
        """Start drawing on canvas"""
        if self.drawing_enabled:
            self.last_x = event.x
            self.last_y = event.y
            
    def draw(self, event):
        """Draw on canvas"""
        if self.drawing_enabled and self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color, width=2, smooth=True
            )
            self.last_x = event.x
            self.last_y = event.y
            
    def stop_drawing(self, event):
        """Stop drawing"""
        self.last_x = None
        self.last_y = None
        
    def save_note(self):
        """Save the note"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.save_location, exist_ok=True)
            
            # Get the text content
            text_content = self.text_area.get("1.0", END)
            
            # Generate filename based on current time
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"note_{timestamp}.txt"
            filepath = os.path.join(self.save_location, filename)
            
            # Save the text content
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(f"Year: {self.year}\n")
                file.write(f"Semester: {self.semester}\n")
                file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("\n" + text_content)
            
            messagebox.showinfo("Success", "Note saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save note: {str(e)}")

    def view_notes(self):
        """Open view notes window"""
        self.root.destroy()  # Close current window
        import view_notes
        view_notes.view_notes_page(self.year, self.semester, self.save_location)
        
    def run(self):
        self.root.mainloop()

def note_taking_page(year, semester, save_location):
    app = NoteTakingApp(year, semester, save_location)
    app.run()
