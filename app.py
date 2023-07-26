import customtkinter
import tkinter
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
import io

from inventree.part import Part
from inventree.stock import StockItem, StockLocation
import inventree

from item_info import ItemInfo
import api_utils

# TODO: Move to .env file
URL = "http://172.25.32.72:8000"


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

        self.stockitem_code = ""
        self.scanner_buffer = ""

    def get_input(self, event):
        if event.char in "0123456789":
            self.scanner_buffer += event.char
        else:
            self.stockitem_code = self.scanner_buffer
            item_info = ItemInfo.from_api(self.api, self.stockitem_code)
            img = api_utils.get_part_img(self.api, URL + item_info.img_path)

            self.set_new_stock_item(item_info, img)

            self.scanner_buffer = ""

    def set_new_stock_item(self, item_info: ItemInfo, img: Image):
        self.part_frame.set_part_details(item_info, img)


class PartDisplay(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(0, weight=4, uniform="top_down")
        self.rowconfigure(1, weight=1, uniform="top_down")
        self.columnconfigure(1, weight=1)

        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="ns")

        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="news")

        self.info_data = customtkinter.CTkLabel(self.info_frame, text="")
        self.info_data.grid()

        self.util_frame = customtkinter.CTkFrame(self)
        self.util_frame.grid(row=1, padx=10, pady=(5, 10), sticky="ews", columnspan=2)

        self.image_label = customtkinter.CTkLabel(self.image_frame, text="")
        self.image_label.grid()
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_part_details(self, id, image):
        self.info_data.configure(text=id)
        image = customtkinter.CTkImage(light_image=image, size=(300, 300))
        self.image_label.configure(image=image)
