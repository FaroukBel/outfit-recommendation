import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from recognition_module import *
import numpy as np
import json

class WardrobeApp:
    """
    This class is for managing clothes and making outfit recommendations.
    """
    def __init__(self):
        self.top = []
        self.bottom = []
        self.shoes = []
        self.item_id = 1  # Start item ID from 1

    def add_photos_from_folder(self, folder_path):
        """
        Adds all photos from the specified folder to the wardrobe.
        """
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                sub, info, res_place_holder = single_classification(file_path)
                item_data = {
                    'id': self.item_id,
                    'path': file_path,
                    'info': info,
                    'res_place_holder': res_place_holder
                }
                if sub == "top":
                    self.top.append(item_data)
                elif sub == "bottom":
                    self.bottom.append(item_data)
                elif sub == "foot":
                    self.shoes.append(item_data)

                self.item_id += 1  # Increment the item ID

    def generate_outfit(self):
        """
        Generates and returns an outfit recommendation based on the available items.
        """
        toseason = "summer"  # Example season, replace with your logic

        top_right_season = [i for i in self.top if i['res_place_holder'][3] == toseason]
        ad_top = top_right_season[np.random.randint(len(top_right_season))] if top_right_season else self.top[np.random.randint(len(self.top))]

        helper_bot = [i for i in self.bottom if i['res_place_holder'][4] == ad_top['res_place_holder'][4]]
        helper_sho = [i for i in self.shoes if i['res_place_holder'][4] == ad_top['res_place_holder'][4]]

        ad_bot = helper_bot[np.random.randint(len(helper_bot))] if helper_bot else self.bottom[np.random.randint(len(self.bottom))]
        ad_sho = helper_sho[np.random.randint(len(helper_sho))] if helper_sho else self.shoes[np.random.randint(len(self.shoes))]

        return ad_top['path'], ad_bot['path'], ad_sho['path']  # Return file paths

    def export_to_json(self, output_file):
        """
        Exports the wardrobe items to a JSON file.
        """
        data = {
            'top': self.top,
            'bottom': self.bottom,
            'shoes': self.shoes
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

    def import_from_json(self, input_file):
        """
        Imports wardrobe items from a JSON file.
        """
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        self.top = [data.get("top", {})]
        self.bottom = [data.get("bottom", {})]
        self.shoes = [data.get("shoes", {})]

class WardrobeAppUI:
    def __init__(self, root):
        self.app = WardrobeApp()
        self.root = root
        self.root.title("Wardrobe App")
        
        # Frame for buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.add_folder_button = tk.Button(frame, text="Add Photos from Folder", command=self.add_photos)
        self.add_folder_button.pack(side=tk.LEFT, padx=10)

        self.generate_button = tk.Button(frame, text="Generate Outfit", command=self.generate_outfit)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.export_button = tk.Button(frame, text="Export to JSON", command=self.export_to_json)
        self.export_button.pack(side=tk.LEFT, padx=10)

        self.import_button = tk.Button(frame, text="Import from JSON", command=self.import_from_json)
        self.import_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        # Frame for displaying outfit images
        self.outfit_frame = tk.Frame(self.root)
        self.outfit_frame.pack(pady=20)

        self.top_image_label = tk.Label(self.outfit_frame)
        self.top_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.bottom_image_label = tk.Label(self.outfit_frame)
        self.bottom_image_label.grid(row=0, column=1, padx=10, pady=10)

        self.shoes_image_label = tk.Label(self.outfit_frame)
        self.shoes_image_label.grid(row=0, column=2, padx=10, pady=10)

    def add_photos(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.app.add_photos_from_folder(folder_path)
            messagebox.showinfo("Success", "Photos added successfully.")

    def generate_outfit(self):
        if not (self.app.top and self.app.bottom and self.app.shoes):
            messagebox.showwarning("Warning", "Please add photos first.")
            return

        top_path, bottom_path, shoes_path = self.app.generate_outfit()
        self.display_image(self.top_image_label, top_path)
        self.display_image(self.bottom_image_label, bottom_path)
        self.display_image(self.shoes_image_label, shoes_path)

    def display_image(self, label, image_path):
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    def export_to_json(self):
        output_file = filedialog.asksaveasfilename(
            title="Save JSON File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if output_file:
            self.app.export_to_json(output_file)
            messagebox.showinfo("Success", f"Data exported to {output_file}")

    def import_from_json(self):
        input_file = filedialog.askopenfilename(
            title="Open JSON File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if input_file:
            self.app.import_from_json(input_file)
            self.display_image(self.top_image_label, self.app.top[0]['info'].split(',')[-1].strip())
            self.display_image(self.bottom_image_label, self.app.bottom[0]['info'].split(',')[-1].strip())
            self.display_image(self.shoes_image_label, self.app.shoes[0]['info'].split(',')[-1].strip())
            messagebox.showinfo("Success", "Data imported successfully.")

def main():
    root = tk.Tk()
    app_ui = WardrobeAppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
