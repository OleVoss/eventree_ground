import customtkinter
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)

        self.title("inventree scanner")
        self.geometry("800x480")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config(background="lightgray")

        self.part_frame = PartDisplay(self)
        self.part_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.part_frame.configure(fg_color="skyblue", bg_color="lightgray")


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

        self.util_frame = customtkinter.CTkFrame(self)
        self.util_frame.grid(row=1, padx=10, pady=(5, 10),
                             sticky="ews", columnspan=2)
