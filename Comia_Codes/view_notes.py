from tkinter import *
from tkinter import ttk, messagebox
import os

def view_notes_page(year, semester, save_location):
    root = Tk()
    root.title("View Notes")
    root.geometry("1000x600+300+200")
    root.configure(bg="#2B777B")
    
    # Create main frame
    main_frame = Frame(root, bg="#2B777B")
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    Label(main_frame, 
          text=f"Notes for {year} - {semester}",
          font=("Microsoft Yahei UI Light", 20, "bold"),
          fg="white",
          bg="#2B777B").pack(pady=(0, 20))
    
    # Create list frame
    list_frame = Frame(main_frame, bg="white")
    list_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    # Create notes listbox with scrollbar
    notes_list = Listbox(list_frame,
                        font=("Microsoft Yahei UI Light", 12),
                        selectmode=SINGLE,
                        bg="white",
                        fg="#2B777B")
    scrollbar = Scrollbar(list_frame)
    
    notes_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=notes_list.yview)
    
    notes_list.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Create preview frame
    preview_frame = Frame(main_frame, bg="white")
    preview_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    
    # Create preview text area with scrollbar
    preview_text = Text(preview_frame,
                       font=("Microsoft Yahei UI Light", 12),
                       wrap=WORD,
                       bg="white",
                       fg="#2B777B")
    preview_scrollbar = Scrollbar(preview_frame)
    
    preview_text.config(yscrollcommand=preview_scrollbar.set)
    preview_scrollbar.config(command=preview_text.yview)
    
    preview_text.pack(side=LEFT, fill=BOTH, expand=True)
    preview_scrollbar.pack(side=RIGHT, fill=Y)
    
    def load_notes():
        """Load notes from the save location"""
        notes_list.delete(0, END)
        if not os.path.exists(save_location):
            return
            
        for filename in os.listdir(save_location):
            if filename.endswith('.txt'):
                notes_list.insert(END, filename)
    
    def show_preview(event):
        """Show preview of selected note"""
        selection = notes_list.curselection()
        if not selection:
            return
            
        filename = notes_list.get(selection[0])
        filepath = os.path.join(save_location, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                preview_text.delete('1.0', END)
                preview_text.insert('1.0', content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load note: {str(e)}")
    
    def delete_note():
        """Delete selected note"""
        selection = notes_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to delete")
            return
            
        filename = notes_list.get(selection[0])
        filepath = os.path.join(save_location, filename)
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            try:
                os.remove(filepath)
                load_notes()
                preview_text.delete('1.0', END)
                messagebox.showinfo("Success", "Note deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note: {str(e)}")
    
    def back_to_note_taking():
        """Return to note taking page"""
        root.destroy()
        import note_taking
        note_taking.note_taking_page(year, semester, save_location)
    
    # Create buttons frame
    button_frame = Frame(main_frame, bg="#2B777B")
    button_frame.pack(side=BOTTOM, fill=X, pady=(20, 0))
    
    # Add buttons
    Button(button_frame,
           text="Delete Note",
           command=delete_note,
           font=("Microsoft Yahei UI Light", 12),
           bg="#1F5C5E",
           fg="white").pack(side=LEFT, padx=5)
           
    Button(button_frame,
           text="Back to Note Taking",
           command=back_to_note_taking,
           font=("Microsoft Yahei UI Light", 12),
           bg="#1F5C5E",
           fg="white").pack(side=RIGHT, padx=5)
    
    # Bind list selection
    notes_list.bind('<<ListboxSelect>>', show_preview)
    
    # Load notes initially
    load_notes()
    
    root.mainloop()
