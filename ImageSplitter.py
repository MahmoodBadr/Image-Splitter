import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from PIL import Image
import os

class ImageSplitterApp:
    def __init__(self, root):
        self.root = root
        root.title("Image Splitter")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.input_folder_entry = ttk.Entry(self.root, width=40)
        self.input_folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(self.root, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.output_folder_entry = ttk.Entry(self.root, width=40)
        self.output_folder_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(self.root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="Start X Coordinate:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.start_x_entry = ttk.Entry(self.root, width=10)
        self.start_x_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="Start Y Coordinate:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.start_y_entry = ttk.Entry(self.root, width=10)
        self.start_y_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="End X Coordinate:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.end_x_entry = ttk.Entry(self.root, width=10)
        self.end_x_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.root, text="End Y Coordinate:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.end_y_entry = ttk.Entry(self.root, width=10)
        self.end_y_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        ttk.Button(self.root, text="Start Processing", command=self.start_processing).grid(row=6, column=1, pady=20, sticky="ew")

        # Configure columns and rows to expand
        self.root.columnconfigure(1, weight=1)
        for i in range(7):
            self.root.rowconfigure(i, weight=1)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.input_folder_entry.delete(0, tk.END)
        self.input_folder_entry.insert(tk.END, folder_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(tk.END, folder_selected)

    def start_processing(self):
        input_folder = self.input_folder_entry.get()
        output_folder = self.output_folder_entry.get()
        start_x = int(self.start_x_entry.get())
        start_y = int(self.start_y_entry.get())
        end_x = int(self.end_x_entry.get())
        end_y = int(self.end_y_entry.get())

        for filename in os.listdir(input_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(input_folder, filename)
                self.split_image(image_path, output_folder, start_x, start_y, end_x, end_y)

        self.show_message("Image splitting completed!")

    def split_image(self, image_path, output_folder, start_x, start_y, end_x, end_y):
        original_image = Image.open(image_path)
        existing_counters = [int(filename.split('_')[2].split('.')[0]) for filename in os.listdir(output_folder) if filename.startswith('sub_image_')]
        counter = max(existing_counters, default=-1) + 1

        # Ensure end coordinates are within the bounds of the original image
        end_x = min(end_x, original_image.width)
        end_y = min(end_y, original_image.height)

        # Loop through the image and save a single sub-image
        box = (start_x, start_y, end_x, end_y)

        # Ensure the sub-image is within the bounds of the original image
        if self.is_within_bounds(box, original_image.size):
            region = original_image.crop(box)

            # Save the sub-image with a unique name
            sub_image_path = os.path.join(output_folder, f"sub_image_{counter}.png")
            region.save(sub_image_path)

    @staticmethod
    def is_within_bounds(box, original_dimensions):
        return all(0 <= coord < dimension for coord, dimension in zip(box[:2], original_dimensions))

    @staticmethod
    def show_message(message):
        messagebox.showinfo("Processing Completed", message)

def main():
    root = ThemedTk(theme="arc")
    app = ImageSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()