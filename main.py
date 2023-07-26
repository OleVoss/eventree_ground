from app import App

from inventree.api import InvenTreeAPI

TOKEN = "6721d214b5f9ec7b3e33b7ac6a67b1a8de7ef954"
URL = "http://172.25.32.72:8000"

# api = InvenTreeAPI(host=URL, username=USER, password=PASSWORD)
api = InvenTreeAPI(host=URL, token=TOKEN)
app = App(api)
app.mainloop()
