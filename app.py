import customtkinter
import tkinter
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
import io

from inventree.part import Part
from inventree.stock import StockItem, StockLocation
import inventree

from item_info import DetailInfo, ItemInfo
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

        self.config(background="white")

        self.part_frame = PartDisplay(self)
        self.part_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.part_frame.configure(fg_color="white", bg_color="white")

        self.bind("<Key>", self.get_input)

        self.stockitem_code = ""
        self.scanner_buffer = ""

    def get_input(self, event):
        if event.char in "0123456789":
            self.scanner_buffer += event.char
        else:
            self.stockitem_code = self.scanner_buffer
            # self.stockitem_code = 720  # TODO: just for debugging!!!
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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(
            row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew"
        )
        self.image_frame.configure(fg_color="white")

        self.info_frame = DetailsList(self)
        self.info_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="news")
        self.info_frame.configure(fg_color="#f2f2f2")

        self.util_frame = customtkinter.CTkFrame(self)
        self.util_frame.grid(row=1, padx=10, pady=(5, 10), sticky="ews", columnspan=2)
        self.util_frame.configure(fg_color="#f2f2f2")
        util_placeholder = customtkinter.CTkLabel(
            self.util_frame, text="<BUTTONS>", font=("Ubuntu", 30)
        )
        util_placeholder.grid()
        util_placeholder.place(relx=0.5, rely=0.5, anchor="center")

        self.image_label = customtkinter.CTkLabel(self.image_frame, text="")
        self.image_label.grid()
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_part_details(self, item_info: ItemInfo, part_img: Image):
        img_w, img_h = part_img.size
        if img_h < img_w:
            target_width = self.image_frame.winfo_width()
            target_height = self.image_frame.winfo_width() * (img_h / img_w)
        else:
            target_width = self.image_frame.winfo_height() * (img_w / img_h)
            target_height = self.image_frame.winfo_height()

        image = customtkinter.CTkImage(
            light_image=part_img, size=(target_width, target_height)
        )
        self.image_label.configure(image=image)
        self.info_frame.set_details(item_info.details)


class DetailsList(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1, uniform="top_down")
        self.columnconfigure(1, weight=3)

        self.rowconfigure(0, weight=2)
        for i in range(1, len(DetailInfo.ALL_DETAILS)):
            self.rowconfigure(i, weight=1)

        self.title = customtkinter.CTkLabel(self, text="Details", font=("Ubuntu", 22))
        self.title.grid(row=0, column=0, columnspan=2)

        self.name_labels = {}
        self.value_labels = {}

        for i, name in enumerate(DetailInfo.ALL_DETAILS):
            name_label = customtkinter.CTkLabel(self, text=name, font=("Ubuntu", 14))
            name_label.grid(row=i + 1, column=0)
            self.name_labels[name] = name_label

            value_label = customtkinter.CTkLabel(self, text="", font=("Ubuntu", 14))
            value_label.grid(row=i + 1, column=1)
            self.value_labels[name] = value_label

    def set_details(self, detail_dict: dict):
        for detail in detail_dict:
            self.value_labels[detail].configure(text=detail_dict[detail])
