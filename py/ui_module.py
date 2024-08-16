import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from recognition_module import *
import numpy as np

class WardrobeApp:
    """
    This class is for managing clothes and making outfit recommendations.
    """
    def __init__(self):
        self.top = []
        self.bottom = []
        self.shoes = []

    def add_photos_from_folder(self, folder_path):
        """
        Adds all photos from the specified folder to the wardrobe.
        """
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                sub, info, res_place_holder = single_classification(file_path)
                
                if sub == "top":
                    self.top.append((file_path, info, res_place_holder))
                elif sub == "bottom":
                    self.bottom.append((file_path, info, res_place_holder))
                elif sub == "foot":
                    self.shoes.append((file_path, info, res_place_holder))

    def generate_outfit(self):
        """
        Generates and returns an outfit recommendation based on the available items.
        """
        toseason = "summer"  # Example season, replace with your logic

        top_right_season = [i for i in self.top if i[2][3] == toseason]
        ad_top = top_right_season[np.random.randint(len(top_right_season))] if top_right_season else self.top[np.random.randint(len(self.top))]

        helper_bot = [i for i in self.bottom if i[2][4] == ad_top[2][4]]
        helper_sho = [i for i in self.shoes if i[2][4] == ad_top[2][4]]

        ad_bot = helper_bot[np.random.randint(len(helper_bot))] if helper_bot else self.bottom[np.random.randint(len(self.bottom))]
        ad_sho = helper_sho[np.random.randint(len(helper_sho))] if helper_sho else self.shoes[np.random.randint(len(self.shoes))]

        return ad_top[0], ad_bot[0], ad_sho[0]  # Return file paths

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

def main():
    root = tk.Tk()
    app_ui = WardrobeAppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
