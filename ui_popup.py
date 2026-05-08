import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def show_popup(root, image_bytes, title="Diagram Viewer", save_btn_command=None):
    """
    Show a popup window.

    Inputs:
    - root: The parent Tkinter window (the main application window).
    - image_bytes: The image data as bytes.
    - title: The title for the popup window (default is "Diagram Viewer").
    - save_btn_command: The command to execute when the save button is clicked.
    Returns:
    - The popup window instance.
    """
    
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("800x600")
    
    popup.transient(root)
    # popup.grab_set()                # Make the popup modal (block interaction with the main window). May remove this

    image = Image.open(BytesIO(image_bytes))
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(popup, image=photo)
    image_label.image = photo       # Keep a reference to prevent garbage collection
    image_label.pack(expand=True)

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=20)

    if save_btn_command is not None:
        save_button = tk.Button(btn_frame, text="Save Diagram", command=save_btn_command)
        save_button.pack(side=tk.LEFT, pady=10)

    close_button = tk.Button(btn_frame, text="Close", command=popup.destroy)
    close_button.pack(side=tk.LEFT, pady=10)

    return popup