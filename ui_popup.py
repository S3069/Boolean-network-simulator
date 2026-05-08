import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import cairosvg

class ImagePopup: 
    def __init__(self, root, svg_bytes, title="Diagram Viewer", save_btn_command=None):
        """
        Show a popup window.

        Inputs:
        - root: The parent Tkinter window (the main application window).
        - svg_bytes: The SVG data as bytes.
        - title: The title for the popup window (default is "Diagram Viewer").
        - save_btn_command: The command to execute when the save button is clicked.

        Returns:
        - The popup window instance.
        """
        
        # Store parameters as instance variables for later use
        self.root = root
        self.svg_bytes = svg_bytes
        self.title = title
        self.save_btn_command = save_btn_command

        # Create the popup window
        self.popup = tk.Toplevel(root)
        self.popup.title(title)
        self.popup.geometry("800x600")
        self.popup.transient(root)  # Make the popup transient to the main window 

        # Set up image
        self.zoom_scale = 1.0

        # Create the UI elements
        self.create_widgets()
        self.popup.after(100, self.display_image)   # Delay image display to ensure canvas is properly initialized

    # Create buttons
    def create_widgets(self):

        # Setup frame for scroll bars and panning
        self.viewer_frame = tk.Frame(self.popup)
        self.viewer_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.viewer_frame, bg="white")

        self.hori_scroll = tk.Scrollbar(
            self.viewer_frame,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview
        )
        self.vert_scroll = tk.Scrollbar(
            self.viewer_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.vert_scroll.set,
            xscrollcommand=self.hori_scroll.set
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vert_scroll.grid(row=0, column=1, sticky="ns")
        self.hori_scroll.grid(row=1, column=0, sticky="ew")

        self.viewer_frame.rowconfigure(0, weight=1)
        self.viewer_frame.columnconfigure(0, weight=1)

        # Panning binds
        self.canvas.bind("<ButtonPress-1>", self.pan_start)
        self.canvas.bind("<B1-Motion>", self.pan_move)

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
        if self.zoom_scale < 5.0:  # Limit maximum zoom level
            self.zoom_scale *= 1.5  # Increase zoom scale by 50%
            self.display_image()

    def zoom_out(self):
        # No limit on zoom out, incase diagram is very large
        self.zoom_scale /= 1.5  # Decrease zoom scale by 50%
        self.display_image()

    def image_larger_than_canvas(self):
        """
        Check if the current image is larger than the canvas in either dimension.

        Returns:
        - True if the image is larger than the canvas in width or height, False otherwise.
        """
        too_wide = True if self.image_width > self.canvas.winfo_width() else False
        too_tall = True if self.image_height > self.canvas.winfo_height() else False
        return too_wide or too_tall

    def pan_start(self, event):
        if self.image_larger_than_canvas():
            self.canvas.scan_mark(event.x, event.y)

    def pan_move(self, event):
        if self.image_larger_than_canvas():
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def display_image(self):
        # Convert SVG bytes to PNG bytes using cairosvg
        png_bytes = cairosvg.svg2png(
            bytestring=self.svg_bytes,
            scale=self.zoom_scale
        )

        rendered_image = Image.open(BytesIO(png_bytes))
        self.photo = ImageTk.PhotoImage(rendered_image)

        self.image_width, self.image_height = rendered_image.size

        # Clear the canvas and display the new image
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Keeps image centred if image > canvas. Otherwise adjusts relative to image
        if self.image_width < canvas_width:
            x = canvas_width // 2
        else:
            x = self.image_width // 2

        if self.image_height < canvas_height:
            y = canvas_height // 2
        else:
            y = self.image_height // 2    

        self.canvas.create_image(x, y, anchor=tk.CENTER, image=self.photo)

        # Limits scroll to larger of the two
        scroll_width = max(self.image_width, canvas_width)
        scroll_height = max(self.image_height, canvas_height)

        self.canvas.config(scrollregion=(0, 0, scroll_width, scroll_height))


def show_popup(root, svg_bytes, title="Diagram Viewer", save_btn_command=None):
    """
    Show a popup window with the given SVG.

    Inputs:
    - root: The parent Tkinter window (the main application window).
    - svg_bytes: The SVG data as bytes.
    - title: The title for the popup window (default is "Diagram Viewer").
    - save_btn_command: The command to execute when the save button is clicked.
    Returns:
    - The popup window instance.
    """
    return ImagePopup(root, svg_bytes, title, save_btn_command)