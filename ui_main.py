import tkinter as tk
import ui_commands as cmds      # Imports commands (and global variables) from ui_commands.py

# ------
# UI Window
# ------

root = tk.Tk()
root.title("Boolean Network Simulator")
root.geometry("1300x850")

# ----- Layout frames -----
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

separator = tk.Frame(main_frame, width=2, bg="grey")
separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

right_frame = tk.Frame(main_frame, width=500)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
right_frame.pack_propagate(False)  # Prevent frame from resizing to fit content

# ----- Settings variables -----
cyclic_var = tk.BooleanVar(value=False)
canonical_var = tk.BooleanVar(value=False)
depth_var = tk.IntVar(value=10000)
valid_depth_command = root.register(cmds.validate_depth)

# ----- (LEFT) File Selection area -----
top_frame = tk.Frame(left_frame)
top_frame.pack(pady=20)

file_entry = tk.Entry(top_frame, width=32)
file_entry.insert(0, "Select file")
file_entry.pack(side=tk.LEFT, padx=5)

open_btn = tk.Button(
    top_frame, 
    text="Open", 
    command=cmds.select_file)
open_btn.pack(side=tk.LEFT)

# Start Button
load_btn = tk.Button(
    left_frame, 
    text="Load Network", 
    command=cmds.load_network)
load_btn.pack(pady=10)

# ----- (LEFT) Actions Frame -----
action_frame = tk.Frame(left_frame)

# -- (LEFT) Visual Selection --
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
    command=cmds.show_popup_wiring_diagram
)
wiring_btn.pack(side=tk.LEFT, padx=10)

state_btn = tk.Button(
    visual_btn_frame, 
    text="State Transition Diagram", 
    font=("Arial", 10),
    width=20,
    command=cmds.draw_state_diagram
)
state_btn.pack(side=tk.LEFT, padx=10)

# -- (LEFT) Analysis Selection --
analysis_frame = tk.Frame(action_frame)
analysis_frame.pack(pady=(30, 10))

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

# Settings: Max Depth
depth_frame = tk.Frame(settings_frame)
depth_frame.pack(pady=5)

depth_label = tk.Label(depth_frame, text="Max Trace Depth:")
depth_label.pack(side=tk.LEFT, padx=(0, 5))

depth_spinbox = tk.Spinbox(
    depth_frame,
    from_=cmds.min_depth,
    to=cmds.max_depth,
    textvariable=depth_var,
    width=10,
    validate="key",
    validatecommand=(valid_depth_command, "%P")
)
depth_spinbox.pack(side=tk.LEFT)

# Settings: Checkbox Settings
cyclic_checkbox = tk.Checkbutton(
    settings_frame, 
    text="Cyclic Attractors Only", 
    variable=cyclic_var
)
cyclic_checkbox.pack(anchor="w")    # left align

canonical_checkbox = tk.Checkbutton(
    settings_frame, 
    text="Use canonical ordering", 
    variable=canonical_var
)
canonical_checkbox.pack(anchor="w")   # left align

# Buttons for analysis

analysis_btn_frame = tk.Frame(analysis_frame)
analysis_btn_frame.pack()

trace_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Traces", 
    font=("Arial", 10),
    width=20,
    command=cmds.print_traces)
trace_btn.pack(side=tk.LEFT, padx=10)

attractor_btn = tk.Button(
    analysis_btn_frame, 
    text="Export Attractors", 
    font=("Arial", 10),
    width=20,
    command=cmds.print_attractors)
attractor_btn.pack(side=tk.LEFT, padx=10)


# ----- (RIGHT) Status Frame -----
status_title = tk.Label(
    right_frame,
    text="Status:",
    font=("Arial", 11, "bold"),
)
status_title.pack(anchor="nw", pady=(20, 10))    # top left align

status_label = tk.Label(
    right_frame,
    text="No file selected.",
    anchor="nw",
    justify=tk.LEFT,
    wraplength=280
)
status_label.pack(anchor="nw", pady=(0, 10), fill=tk.BOTH)    # top left align

# ----- (RIGHT) Diagram Frame -----

wiring_diagram_title = tk.Label(
    right_frame,
    text="Loaded Network:",
    font=("Arial", 11, "bold")
)

wiring_diagram_img = tk.Label(right_frame)

# ----- Initialize UI Commands -----

cmds.setup_ui(
    root,
    file_entry,
    status_label,
    load_btn,
    action_frame,
    wiring_diagram_img,
    wiring_diagram_title,
    cyclic_var,
    canonical_var,
    depth_var
)

# ------
# Run
# ------

root.mainloop()