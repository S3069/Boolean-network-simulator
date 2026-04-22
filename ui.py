import tkinter as tk
from tkinter import filedialog
import os
from boolean_network_simulator import (
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

min_depth = 1
max_depth = 1000000
default_depth = 10000

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
        traces = runAllTraces(
            state_trans,
            cyclicOnly = cyclic_var.get(),
            canonicalOrder = canonical_var.get(),
            maxDepth = get_depth()
            )
        saveTracesToFile(traces, filepath)

def print_attractors():
    if state_trans is not None:
        attractors = compileAttractors(
            state_trans,
            cyclicOnly = cyclic_var.get(),
            canonicalOrder = canonical_var.get(),
            maxDepth = get_depth()
            )
        saveAttractorsToFile(attractors, filepath)

# ------
# Depth validation functions
# ------

def validate_depth(value):
    # Allow empty string (to allow user to clear the field)
    if value == "":
        return True
    
    # Only allow digits
    if not value.isdigit():
        return False

    # Minimum limit of 1
    if int(value) < min_depth or int(value) > max_depth:
        return False

    return int(value)

def get_depth():
    try:
        value = depth_var.get()
        if value < min_depth or value > max_depth:
            raise ValueError("Depth must be between 1 and 1,000,000.")

        return value
    except (tk.TclError, ValueError):
        return default_depth

# ------
# UI Window
# ------

root = tk.Tk()
root.title("Boolean Network Simulator")
root.geometry("1000x500")

# ----- Layout frames -----
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

separator = tk.Frame(main_frame, width=2, bg="grey")
separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

right_frame = tk.Frame(main_frame, width=300)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
right_frame.pack_propagate(False)  # Prevent frame from resizing to fit content

# ----- Settings variables -----
cyclic_var = tk.BooleanVar(value=False)
canonical_var = tk.BooleanVar(value=False)
depth_var = tk.IntVar(value=10000)
valid_depth_command = root.register(validate_depth)

# ----- File Selection area -----
top_frame = tk.Frame(left_frame)
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
    left_frame, 
    text="Load Network", 
    command=load_network)
load_btn.pack(pady=10)

# ----- Actions Frame -----
action_frame = tk.Frame(left_frame)

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

depth_spinbox = tk.Spinbox(
    depth_frame,
    from_=min_depth,
    to=max_depth,
    textvariable=depth_var,
    width=10,
    validate="key",
    validatecommand=(valid_depth_command, "%P")
)
depth_spinbox.pack(side=tk.LEFT)

# Buttons for analysis

analysis_btn_frame = tk.Frame(analysis_frame)
analysis_btn_frame.pack()

trace_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Traces", 
    font=("Arial", 10),
    width=20,
    command=print_traces)
trace_btn.pack(side=tk.LEFT, padx=10)

attractor_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Attractors", 
    font=("Arial", 10),
    width=20,
    command=print_attractors)
attractor_btn.pack(side=tk.LEFT, padx=10)

# ------
# Run
# ------

root.mainloop()