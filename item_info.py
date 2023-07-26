from inventree.api import InvenTreeAPI
import api_utils


class ItemInfo:
    @staticmethod
    def from_api(api: InvenTreeAPI, stock_item_pk: str):
        item_info = ItemInfo(stock_item_pk)
        item_info.get_data(api)
        return item_info

    def __init__(self, primary_key: str):
        self.pk = primary_key

    def get_data(self, api: InvenTreeAPI):
        stock = api_utils.get_stockitem_fields(api, self.pk)
        part = api_utils.get_part_fields(api, stock["part"])

        self.name = stock["part_detail"]["name"]
        self.description = part["description"]
        self.serial = stock["serial"]
        self.default_location = part["default_location"]
        self.notes = stock["notes"]
        self.note_warn = True if self.notes else False

        self.stock_item_count = part["stock_item_count"]
        self.total_in_stock = part["total_in_stock"]

        self.img_path = part["image"]
