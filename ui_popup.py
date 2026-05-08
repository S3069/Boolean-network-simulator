import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import cairosvg

class ImagePopup: 
    def __init__(self, root, image_bytes, title="Diagram Viewer", save_btn_command=None, is_svg=False):
        """
        Show a popup window.

        Inputs:
        - root: The parent Tkinter window (the main application window).
        - image_bytes: The image data as bytes.
        - title: The title for the popup window (default is "Diagram Viewer").
        - save_btn_command: The command to execute when the save button is clicked.
        - is_svg: A boolean indicating whether the image data is in SVG format.

        Returns:
        - The popup window instance.
        """
        
        # Store parameters as instance variables for later use
        self.root = root
        self.image_bytes = image_bytes
        self.title = title
        self.save_btn_command = save_btn_command
        self.is_svg = is_svg

        # Create the popup window
        self.popup = tk.Toplevel(root)
        self.popup.title(title)
        self.popup.geometry("800x600")
        self.popup.transient(root)  # Make the popup transient to the main window 

        # Set up image
        self.zoom_scale = 1.0
        if not self.is_svg:
            self.image = Image.open(BytesIO(image_bytes))

        # Create the UI elements
        self.create_widgets()
        self.display_image()

    # Create buttons
    def create_widgets(self):
        self.canvas = tk.Canvas(self.popup, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.display_image())  # Redraw image on canvas resize

        self.btn_frame = tk.Frame(self.popup)
        self.btn_frame.pack(pady=10)

        self.zoom_in_btn = tk.Button(
            self.btn_frame,
            text="Zoom In",
            command=self.zoom_in
        )
        self.zoom_in_btn.pack(side=tk.LEFT, padx=5)

        self.zoom_out_btn = tk.Button(
            self.btn_frame,
            text="Zoom Out",
            command=self.zoom_out
        )
        self.zoom_out_btn.pack(side=tk.LEFT, padx=5)

        if self.save_btn_command is not None:
            self.save_btn = tk.Button(
                self.btn_frame,
                text="Save Diagram",
                command=self.save_btn_command
            )
            self.save_btn.pack(side=tk.LEFT, pady=5)

        self.close_btn = tk.Button(
            self.btn_frame,
            text="Close",
            command=self.popup.destroy
        )
        self.close_btn.pack(side=tk.LEFT, pady=5)

    def zoom_in(self):
        self.zoom_scale *= 1.2  # Increase zoom scale by 20%
        self.display_image()

    def zoom_out(self):
        self.zoom_scale /= 1.2  # Decrease zoom scale by 20%
        self.display_image()

    def display_image(self):
        if self.is_svg:
            # Convert SVG bytes to PNG bytes using cairosvg
            png_bytes = cairosvg.svg2png(
                bytestring=self.image_bytes,
                scale=self.zoom_scale
            )
            rendered_image = Image.open(BytesIO(png_bytes))
        else:
            # Resize the image according to the current zoom scale
            width, height = self.image.size
            new_size = (
                int(width * self.zoom_scale),
                int(height * self.zoom_scale)
            )
            rendered_image = self.image.resize(new_size)
        
        self.photo = ImageTk.PhotoImage(rendered_image)

        # Clear the canvas and display the new image
        self.canvas.delete("all")

        x = max(self.canvas.winfo_width() // 2, rendered_image.width // 2)  # Center horizontally
        y = max(self.canvas.winfo_height() // 2, rendered_image.height // 2)  # Center vertically

        self.canvas.create_image(x, y, anchor=tk.CENTER, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

def show_popup(root, image_bytes, title="Diagram Viewer", save_btn_command=None, is_svg=False):
    """
    Show a popup window with the given image.

    Inputs:
    - root: The parent Tkinter window (the main application window).
    - image_bytes: The image data as bytes.
    - title: The title for the popup window (default is "Diagram Viewer").
    - save_btn_command: The command to execute when the save button is clicked.
    - is_svg: A boolean indicating whether the image is an SVG.
    Returns:
    - The popup window instance.
    """
    return ImagePopup(root, image_bytes, title, save_btn_command, is_svg)