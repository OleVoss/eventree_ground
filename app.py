import customtkinter
from PIL import Image

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
            self.part_frame.set_part_details(self.part_code)
            self.part_code = ""
            item_data = self.api.get("/stock/82")
            self.set_new_stock_item(item_data)

    def set_new_stock_item(self, item_data):
        print(item_data)


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

    def set_part_details(self, id):
        self.info_data.configure(text=id)
