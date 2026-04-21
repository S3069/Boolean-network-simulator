import tkinter as tk
from tkinter import filedialog
import os
from SimpleSim import (
    loadNetworkFromFile, 
    drawWiringDiagram, 
    compileStateTransitions, 
    drawStateGraph, 
    compileAttractors, 
    runAllTraces, 
    saveAttractorsToFile, 
    saveTracesToFile
    )

# Global variables
filepath = None
G = None
state_trans = None

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
        file_name = os.path.basename(filepath)
        
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_name) 
        
        # Resets UI to show load button and hide further functions
        action_frame.pack_forget()
        load_btn.pack(pady=10)

# ------
# Button functions
# ------

def load_network():
    global G, state_trans

    # If no file is selected, do nothing
    if not filepath:
        return
    
    # Load the network and compile state transitions
    G = loadNetworkFromFile(filepath)
    state_trans = compileStateTransitions(G)

    # Hide load button
    load_btn.pack_forget()

    # Show command buttons
    action_frame.pack(pady=20)
    

def draw_wiring_diagram():
    if G is not None:
        drawWiringDiagram(G, filepath)

def draw_state_diagram():
    if state_trans is not None:
        drawStateGraph(state_trans, filepath)

def print_traces():
    if state_trans is not None:
        traces = runAllTraces(state_trans)
        saveTracesToFile(traces, filepath)

def print_attractors():
    if state_trans is not None:
        attractors = compileAttractors(state_trans)
        saveAttractorsToFile(attractors, filepath)


# ------
# Window
# ------

root = tk.Tk()
root.title("Boolean Network Simulator")
root.geometry("550x380")

# Settings variables
cyclic_var = tk.BooleanVar(value=False)
canonical_var = tk.BooleanVar(value=False)
max_depth_var = tk.IntVar(value=10000)

# (TOP) File Selection area
top_frame = tk.Frame(root)
top_frame.pack(pady=20)

file_entry = tk.Entry(top_frame, width=32)
file_entry.insert(0, "Select file")
file_entry.pack(side=tk.LEFT, padx=5)

open_btn = tk.Button(
    top_frame, 
    text="Open", 
    command=select_file)
open_btn.pack(side=tk.LEFT)

# Start Button
load_btn = tk.Button(
    root, 
    text="Load Network", 
    command=load_network)
load_btn.pack(pady=10)

# (MAIN) Actions Frame
action_frame = tk.Frame(root)

# --- Visual Selection ---
visual_frame = tk.Frame(action_frame)
visual_frame.pack(pady=10)

visual_label = tk.Label(
    visual_frame,
    text="Visualize Network",
    width=25,
    font=("Arial", 11, "bold")
)
visual_label.pack(pady=(0, 10))

# Buttons for visualizations

visual_btn_frame = tk.Frame(visual_frame)
visual_btn_frame.pack()

wiring_btn = tk.Button(
    visual_btn_frame, 
    text="Wiring Diagram", 
    font=("Arial", 10),
    width=20,
    command=draw_wiring_diagram
)
wiring_btn.pack(side=tk.LEFT, padx=10)

state_btn = tk.Button(
    visual_btn_frame, 
    text="State Transition Diagram", 
    font=("Arial", 10),
    width=20,
    command=draw_state_diagram
)
state_btn.pack(side=tk.LEFT, padx=10)

# --- Analysis Selection ---
analysis_frame = tk.Frame(action_frame)
analysis_frame.pack(pady=10)

analysis_label = tk.Label(
    analysis_frame,
    text="Analyse Network Dynamics",
    width=25,
    font=("Arial", 11, "bold")
)
analysis_label.pack(pady=(0, 10))

# Settings for analysis
settings_frame = tk.Frame(analysis_frame)
settings_frame.pack(pady=5)

# Settings: Checkbox Settings
cyclic_checkbox = tk.Checkbutton(
    settings_frame, 
    text="Cyclic Attractors Only", 
    variable=cyclic_var
)
cyclic_checkbox.pack(anchor="w")

canonical_checkbox = tk.Checkbutton(
    settings_frame, 
    text="Use canonical ordering", 
    variable=canonical_var
)
canonical_checkbox.pack(anchor="w")

# Settings: Max Depth
depth_frame = tk.Frame(settings_frame)
depth_frame.pack(pady=5)

depth_label = tk.Label(depth_frame, text="Max Trace Depth:")
depth_label.pack(side=tk.LEFT, padx=(0, 5))

depth_entry = tk.Entry(depth_frame, textvariable=max_depth_var, width=10)
depth_entry.pack(side=tk.LEFT)

# Buttons for analysis

analysis_btn_frame = tk.Frame(analysis_frame)
analysis_btn_frame.pack()

trace_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Traces", 
    font=("Arial", 10),
    width=20,command=print_traces)
trace_btn.pack(side=tk.LEFT, padx=10)

attractor_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Attractors", 
    font=("Arial", 10),
    width=20,    command=print_attractors)
attractor_btn.pack(side=tk.LEFT, padx=10)

# ------
# Run
# ------

root.mainloop()