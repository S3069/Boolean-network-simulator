import tkinter as tk

def show_popup(parent, title="Diagram Viewer"):
    """
    Show a popup window.

    Inputs:
    - parent: The parent Tkinter window (e.g., the main application window).
    - title: The title for the popup window (default is "Diagram Viewer").

    Returns:
    - The popup window instance.
    """
    
    popup = tk.Toplevel(parent)
    popup.title(title)
    popup.geometry("800x600")
    
    popup.transient(parent)
    popup.grab_set()            # Make the popup modal (block interaction with the main window). May remove this

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=20)

    return popup