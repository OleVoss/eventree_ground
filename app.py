import customtkinter
from PIL import Image
from imageio import imread
import requests
import io

from inventree.part import Part
from inventree.stock import StockItem, StockLocation


class App(customtkinter.CTk):
    def __init__(self, api):
        super().__init__()
        self.attributes("-fullscreen", False)

        self.api = api

        self.title("inventree scanner")
        self.geometry("800x480")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config(background="lightgray")

        self.part_frame = PartDisplay(self)
        self.part_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.part_frame.configure(fg_color="skyblue", bg_color="lightgray")

        self.bind("<Key>", self.get_input)

        self.part_code = ""

    def get_input(self, event):
        if event.char in "0123456789":
            self.part_code += event.char
        else:
            self.part_code = ""
            item_data = self.api.get("/stock/82")
            part_data = self.api.get("/part/82")
            img_path = part_data["image"]
            img_path = "https://demo.inventree.org" + img_path
            r = requests.get(img_path, stream=True)
            img = Image.open(io.BytesIO(r.content))
            self.set_new_stock_item(item_data, img)

    def set_new_stock_item(self, item_data, img):
        self.part_frame.set_part_details(item_data, img)


class PartDisplay(customtkinter.CTkFrame):
    def __init__(self, master):

        super().__init__(master)

        self.rowconfigure(0, weight=4, uniform="top_down")
        self.rowconfigure(1, weight=1, uniform="top_down")
        self.columnconfigure(1, weight=1)

        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=(
            10, 5), pady=(10, 5), sticky="ns")

        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=0, column=1, padx=(
            5, 10), pady=(10, 5), sticky="news")

        self.info_data = customtkinter.CTkLabel(
            self.info_frame)
        self.info_data.grid()

        self.util_frame = customtkinter.CTkFrame(self)
        self.util_frame.grid(row=1, padx=10, pady=(5, 10),
                             sticky="ews", columnspan=2)

        self.image_label = customtkinter.CTkLabel(self.image_frame)
        self.image_label.grid()

    def set_part_details(self, id, image):
        self.info_data.configure(text=id)
        image = customtkinter.CTkImage(light_image=image, size=(50, 50))
        self.image_label.configure(image=image)
