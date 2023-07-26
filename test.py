import pprint
from inventree.api import InvenTreeAPI
from inventree.stock import StockItem
from inventree.part import Part, PartCategory

import api_utils
from item_info import ItemInfo

TOKEN = "6721d214b5f9ec7b3e33b7ac6a67b1a8de7ef954"
URL = "http://172.25.32.72:8000"

api = InvenTreeAPI(host=URL, token=TOKEN)

item_info = ItemInfo.from_api(api, 730)
print(item_info.description)
