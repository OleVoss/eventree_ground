from app import App

from inventree.api import InvenTreeAPI


URL = "https://demo.inventree.org"
USER = "engineer"
PASSWORD = "partsonly"

api = InvenTreeAPI(host=URL, username=USER, password=PASSWORD)

app = App(api)
app.mainloop()
