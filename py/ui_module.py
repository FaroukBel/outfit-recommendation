from recognition_module import *

class WardrobeApp:
    """
    This class is for managing clothes and making outfit recommendations.
    """
    def __init__(self):
        self.top = []
        self.bottom = []
        self.shoes = []

    def add_photo(self):
        """
        Prompts the user for a file path, performs classification, and adds the result to the appropriate list.
        """
        file_path = input("Enter the path of the photo: ")
        sub, info, res_place_holder = single_classification(file_path)
        
        if sub == "top":
            self.top.append(res_place_holder)
            print(f"Added top: {info}")
        elif sub == "bottom":
            self.bottom.append(res_place_holder)
            print(f"Added bottom: {info}")
        elif sub == "foot":
            self.shoes.append(res_place_holder)
            print(f"Added shoes: {info}")

    def edit_item(self, item_list, item_type):
        """
        Allows the user to edit an item in the specified list.
        """
        if not item_list:
            print(f"No {item_type} items to edit.")
            return
        
        print(f"Current {item_type} items:")
        for i, item in enumerate(item_list, 1):
            print(f"{i}. {item[1]}")

        item_index = int(input(f"Select a {item_type} item to edit (1-{len(item_list)}): ")) - 1
        new_text = input(f"Enter the new text for this {item_type}: ")

        item_list[item_index] = (*item_list[item_index][:-1], new_text)
        print(f"Updated {item_type} item to: {new_text}")

    def delete_item(self, item_list, item_type):
        """
        Allows the user to delete an item from the specified list.
        """
        if not item_list:
            print(f"No {item_type} items to delete.")
            return
        
        print(f"Current {item_type} items:")
        for i, item in enumerate(item_list, 1):
            print(f"{i}. {item[1]}")

        item_index = int(input(f"Select a {item_type} item to delete (1-{len(item_list)}): ")) - 1
        deleted_item = item_list.pop(item_index)
        print(f"Deleted {item_type} item: {deleted_item[1]}")

    def generate_outfit(self):
        """
        Generates and displays an outfit recommendation based on the available items.
        """
        toseason = "summer"  # Example season, replace with your logic

        top_right_season = [i for i in self.top if i[3] == toseason]
        ad_top = top_right_season[np.random.randint(len(top_right_season))] if top_right_season else self.top[np.random.randint(len(self.top))]

        helper_bot = [i for i in self.bottom if i[4] == ad_top[4]]
        helper_sho = [i for i in self.shoes if i[4] == ad_top[4]]

        ad_bot = helper_bot[np.random.randint(len(helper_bot))] if helper_bot else self.bottom[np.random.randint(len(self.bottom))]
        ad_sho = helper_sho[np.random.randint(len(helper_sho))] if helper_sho else self.shoes[np.random.randint(len(self.shoes))]

        print("Today's Outfit Recommendation:")
        print(f"Top: {ad_top[-1]}")
        print(f"Bottom: {ad_bot[-1]}")
        print(f"Shoes: {ad_sho[-1]}")

def run():
    app = WardrobeApp()

    while True:
        print("\nOptions:")
        print("1. Add a photo")
        print("2. Edit a top")
        print("3. Edit a bottom")
        print("4. Edit shoes")
        print("5. Delete a top")
        print("6. Delete a bottom")
        print("7. Delete shoes")
        print("8. Generate today's outfit recommendation")
        print("9. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            app.add_photo()
        elif choice == "2":
            app.edit_item(app.top, "top")
        elif choice == "3":
            app.edit_item(app.bottom, "bottom")
        elif choice == "4":
            app.edit_item(app.shoes, "shoes")
        elif choice == "5":
            app.delete_item(app.top, "top")
        elif choice == "6":
            app.delete_item(app.bottom, "bottom")
        elif choice == "7":
            app.delete_item(app.shoes, "shoes")
        elif choice == "8":
            app.generate_outfit()
        elif choice == "9":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    run()
