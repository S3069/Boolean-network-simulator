import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

class ImagePopup: 
    def __init__(self, root, image_bytes, title="Diagram Viewer", save_btn_command=None):
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
        
        # Store parameters as instance variables for later use
        self.root = root
        self.image_bytes = image_bytes
        self.title = title
        self.save_btn_command = save_btn_command

        # Create the popup window
        self.popup = tk.Toplevel(root)
        self.popup.title(title)
        self.popup.geometry("800x600")
        self.popup.transient(root)  # Make the popup transient to the main window 

        # Set up image
        self.image = Image.open(BytesIO(image_bytes))
        self.zoom_scale = 1.0

        self.create_widgets()

        # Create buttons
        def create_widgets(self):
            self.canvas = tk.Canvas(self.popup, bg="white")
            self.canvas.pack(fill=tk.BOTH, expand=True)

            self.btn_frame = tk.Frame(self.popup)
            self.btn_frame.pack(pady=10)

            if self.save_btn_command is not None:
                self.save_btn = tk.Button(
                    self.btn_frame,
                    text="Save Diagram",
                    command=self.save_btn_command
                )
                self.save_btn.pack(side=tk.LEFT, pady=10)

            self.close_btn = tk.Button(
                self.btn_frame,
                text="Close",
                command=self.popup.destroy
            )
            self.close_btn.pack(side=tk.LEFT, pady=10)




'''TODO: format the rest of code:'''
################
    

    image = Image.open(BytesIO(image_bytes))
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(popup, image=photo)
    image_label.image = photo       # Keep a reference to prevent garbage collection
    image_label.pack(expand=True)

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=20)





    return popup