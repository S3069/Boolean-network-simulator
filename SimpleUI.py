import tkinter as tk
from tkinter import filedialog
import os

# File path of the selected file
selected_file_path = None

# ------
# Open file
# ------

def open_file():
    global selected_file_path
    
    filepath = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    
    # If a file was selected, update the entry field and store the path
    if filepath:
        selected_file_path = filepath
        
        # Displays only file name
        file_name = os.path.basename(filepath)
        
        file_entry.delete(0, tk.END)        # Clear existing text from field
        file_entry.insert(0, file_name)     # Insert new file name into field
        
        start_button.pack(pady=10)

# ------
# Button functions
# ------

def start_processing():
    global selected_file_path
    
    if not selected_file_path:
        return
    
    # Add input/parser function from SimpleSim.py
    # ttables = fileInputNodes(selected_file_path)      # Find how to run this command

    # Hide start button
    start_button.pack_forget()

def draw_network():
    # Add draw network function from SimpleSim.py
    pass

def print_traces():
    # Add print traces function from SimpleSim.py
    pass

def print_attractors():
    # Add print attractors function from SimpleSim.py
    pass


# ------
# Window
# ------

root = tk.Tk()
root.title("Boolean Network Simulator")
root.geometry("500x250")

top_frame = tk.Frame(root)
top_frame.pack(pady=20)

file_entry = tk.Entry(top_frame, width=30)
file_entry.insert(0, "Select file")
file_entry.pack(side=tk.LEFT, padx=5)

open_button = tk.Button(top_frame, text="Open", command=open_file)
open_button.pack(side=tk.LEFT)

#  Start Button
start_button = tk.Button(root, text="Start", command=start_processing)


# ------
# Run
# ------

root.mainloop()