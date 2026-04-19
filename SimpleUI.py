import tkinter as tk
from tkinter import filedialog
import os
from SimpleSim import loadNetworkFromFile, drawWiringDiagram, compileStateTransitions, drawStateGraph, compileAttractors, runAllTraces, saveAttractorsToFile, saveTracesToFile

# File path of the selected file
selected_file_path = None

# ------
# Open file
# ------

def select_file():
    global filepath
    
    filepath = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    
    # If a file was selected, update the entry field and store the path
    if filepath:
        
        # Displays only file name
        file_name = os.path.basename(filepath)
        
        file_entry.delete(0, tk.END)        # Clear existing text from field
        file_entry.insert(0, file_name)     # Insert new file name into field
        
        # Resets UI to show start button and hide further functions
        actions_frame.pack_forget()
        start_btn.pack(pady=10)

# ------
# Button functions
# ------

def load_network():
    # If no file is selected, do nothing
    if not filepath:
        return
    
    # Load the network and compile state transitions
    global G, state_trans
    G = loadNetworkFromFile(filepath)
    state_trans = compileStateTransitions(G)

    # Hide start button
    start_btn.pack_forget()

    # Show command buttons
    actions_frame.pack(pady=20)
    

def draw_wiring_diagram():
    drawWiringDiagram(G, filepath)

def draw_state_diagram():
    drawStateGraph(state_trans, filepath)

def print_traces():
    traces = runAllTraces(state_trans)
    saveTracesToFile(traces, filepath)

def print_attractors():
    attractors = compileAttractors(state_trans)
    saveAttractorsToFile(attractors, filepath)


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

open_btn = tk.Button(top_frame, text="Open", command=select_file)
open_btn.pack(side=tk.LEFT)

#  Start Button
start_btn = tk.Button(root, text="Start", command=load_network)

# Action Selection Buttons
actions_frame = tk.Frame(root)

draw_btn = tk.Button(actions_frame, text="Draw Wiring Diagram", command=draw_wiring_diagram)
draw_btn.pack(side=tk.LEFT, padx=10)

draw_state_btn = tk.Button(actions_frame, text="Draw State Diagram", command=draw_state_diagram)
draw_state_btn.pack(side=tk.LEFT, padx=10)

trace_btn = tk.Button(actions_frame, text="Print Traces", command=print_traces)
trace_btn.pack(side=tk.LEFT, padx=10)

attractor_btn = tk.Button(actions_frame, text="Print Attractors", command=print_attractors)
attractor_btn.pack(side=tk.LEFT, padx=10)

# ------
# Run
# ------

root.mainloop()