import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from io import BytesIO

from boolean_network_simulator import (
    loadNetworkFromFile, 
    createStateGraph, 
    getGraphImageBytes,
    saveWiringDiagram,
    saveStateGraph,
    compileStateTransitions, 
    runAllTraces, 
    compileAttractors, 
    saveTracesToFile,
    saveAttractorsToFile
)

from ui_popup import show_popup

# Global variables
filepath = None
G = None
state_trans = None

min_depth = 1
max_depth = 1000000
default_depth = 10000

root = None

# Widgets from ui_main that need to be accessed in commands
file_entry=None
status_label=None
load_btn=None
action_frame=None
wiring_diagram_img=None
wiring_diagram_title=None

cyclic_var=None
canonical_var=None
depth_var=None

def setup_ui(
        given_root,
        given_file_entry,
        given_status_label,
        given_load_btn,
        given_action_frame,
        given_wiring_diagram_img,
        given_wiring_diagram_title,
        given_cyclic_var,
        given_canonical_var,
        given_depth_var,
):
    global root
    global file_entry, status_label, load_btn, action_frame
    global wiring_diagram_img, wiring_diagram_title
    global cyclic_var, canonical_var, depth_var

    root = given_root
    file_entry = given_file_entry
    status_label = given_status_label
    load_btn = given_load_btn
    action_frame = given_action_frame
    wiring_diagram_img = given_wiring_diagram_img
    wiring_diagram_title = given_wiring_diagram_title
    cyclic_var = given_cyclic_var
    canonical_var = given_canonical_var
    depth_var = given_depth_var

# ------
# Open file
# ------

def select_file():
    """
    Open a file dialog to select a Boolean network file, and update the UI accordingly.
    """
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
        
        # Resets UI to show load button and hide further features
        resetUI()
        setStatus(f"File selected: {filepath}")

# ------
# Button functions
# ------

def load_network():
    """
    Load the Boolean network from the selected file, compile state transitions, and update the UI with the wiring diagram.
    """
    global G, state_trans

    # If no file is selected, do nothing
    if not filepath:
        return
    
    '''
    TODO: Add error handling for invalid file formats, and display error messages in the status box.
    '''
    
    # Load the network and compile state transitions
    G = loadNetworkFromFile(filepath)
    state_trans = compileStateTransitions(G)

    # Create the wiring diagram
    image_bytes = getGraphImageBytes(G)
    wiring_diagram = resize_image_bytes(image_bytes)

    revealUI(wiring_diagram)
    setStatus(f"File loaded: {filepath}")
    

def show_popup_wiring_diagram():
    """
    Open the wiring diagram in a popup window, then update the status message.
    """
    if G is not None:
        image_bytes = getGraphImageBytes(G)
        show_popup(
            root=root,
            image_bytes=image_bytes,
            title="Wiring Diagram",
            save_btn_command=lambda:setStatus(saveWiringDiagram(image_bytes=image_bytes, filename=filepath))
        )

        message = f"Wiring diagram opened in popup window."
        setStatus(message)

def show_popup_state_diagram():
    """
    Open the state diagram in a popup window, then update the status message.
    """
    if state_trans is not None:
        SG = createStateGraph(state_trans)
        image_bytes = getGraphImageBytes(SG)
        show_popup(
            root=root,
            image_bytes=image_bytes,
            title="State Transition Diagram",
            save_btn_command=lambda:setStatus(saveStateGraph(image_bytes=image_bytes, filename=filepath))
        )

        message = f"State transition diagram opened in popup window."
        setStatus(message)

def print_traces():
    """
    Run all traces of the Boolean network and save them to a file, then update the status message.
    """
    if state_trans is not None:
        traces = runAllTraces(
            state_trans,
            cyclicOnly = cyclic_var.get(),
            canonicalOrder = canonical_var.get(),
            maxDepth = get_depth()
            )
        
        message = saveTracesToFile(traces, filepath)
        setStatus(message)

def print_attractors():
    """
    Compile attractors from the Boolean network and save them to a file, then update the status message.
    """
    if state_trans is not None:
        attractors = compileAttractors(
            state_trans,
            cyclicOnly = cyclic_var.get(),
            canonicalOrder = canonical_var.get(),
            maxDepth = get_depth()
            )
        
        message = saveAttractorsToFile(attractors, filepath)
        setStatus(message)


# ------
# Depth validation functions
# ------

def validate_depth(value):
    """
    Validate the input for the depth spinbox to ensure it's a positive integer within the specified range. 
    Values are set to:
    - minimum of 1
    - maximum of 1,000,000
    - default of 10,000

    Input:
    - value: the input string from the spinbox

    Output:
    - True if the input is valid (empty string or a valid integer within range), False otherwise
    """
    # Allow empty string (to allow user to clear the field)
    if value == "":
        return True
    
    # Only allow digits
    if not value.isdigit():
        return False

    # Minimum limit of 1
    if int(value) < min_depth or int(value) > max_depth:
        return False

    return True

def get_depth():
    """
    Get the current value of the depth variable, ensuring it is within the valid range. If the value is invalid (e.g., non-integer, out of range), return the default depth.
    
    Output:
    - The valid depth value from the spinbox, or the default depth if the input is invalid
    """
    try:
        value = depth_var.get()
        if value < min_depth or value > max_depth:
            raise ValueError("Depth must be between 1 and 1,000,000.")

        return value
    except (tk.TclError, ValueError):
        return default_depth


# ------
# Status update function
# ------

def setStatus(message):
    """
    Update the status label with the provided message.
    
    Input:
    - message: the string message to display in the status label
    """
    status_label.config(text=message)


# ------
# Image resizer function
# ------

def resize_image_bytes(image_bytes, max_width=500, max_height=600):
    """
    Resize an image from bytes while preserving aspect ratio. Return a PhotoImage for Tkinter.
    
    Input:
    - image_bytes: the image data in bytes format
    - max_width: the maximum width for the resized image (default is 500 pixels)
    - max_height: the maximum height for the resized image (default is 600 pixels)
    
    Output:
    - A PhotoImage object that can be used in Tkinter to display the resized image
    """
    image = Image.open(BytesIO(image_bytes))

    # Resize the image while preserving aspect ratio
    image.thumbnail((max_width, max_height))

    return ImageTk.PhotoImage(image)


# ------
# UI update functions
# ------

def resetUI():
    """
    Reset the UI to the initial state after a new file is selected.

    Hides action buttons and clears the wiring diagram.
    """
    # Hide action buttons, show load button
    action_frame.pack_forget()
    load_btn.pack(pady=10)

    # Hide and clear wiring diagram
    wiring_diagram_title.pack_forget()
    wiring_diagram_img.config(image="") 
    wiring_diagram_img.pack_forget()

def revealUI(wiring_diagram):
    """
    Reveal the action buttons and display the wiring diagram after a file is loaded.

    Hides the load button.
    
    Input:
    - wiring_diagram: a PhotoImage object representing the wiring diagram to be displayed
    """
    # Show action buttons, hide load button
    load_btn.pack_forget()
    action_frame.pack(pady=20)

    # Display the wiring diagram
    wiring_diagram_title.pack(anchor="nw", pady=(20, 10))
    wiring_diagram_img.config(image=wiring_diagram)
    wiring_diagram_img.pack()
    wiring_diagram_img.image = wiring_diagram  # Keep a reference to prevent garbage collection
