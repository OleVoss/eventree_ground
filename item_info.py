from inventree.api import InvenTreeAPI
import api_utils


class DetailInfo:
    NAME = "Name"
    DESCRIPTION = "Description"
    SERIAL_NO = "Serial No."
    DEFAULT_LOCATION = "Default location"
    NOTES = "Notes"
    NOTE_WARN = "Note warn"
    CURRENTLY_IN_STOCK = "Currently in stock"
    TOTAL_IN_STOCK = "Total in stock"

    ALL_DETAILS = [
        NAME,
        DESCRIPTION,
        SERIAL_NO,
        DEFAULT_LOCATION,
        NOTES,
        NOTE_WARN,
        CURRENTLY_IN_STOCK,
        TOTAL_IN_STOCK,
    ]


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

        self.details = {
            DetailInfo.NAME: self.name,
            DetailInfo.DESCRIPTION: self.description,
            DetailInfo.SERIAL_NO: self.serial,
            DetailInfo.DEFAULT_LOCATION: self.default_location,
            DetailInfo.NOTES: self.notes,
            DetailInfo.NOTE_WARN: self.note_warn,
            DetailInfo.CURRENTLY_IN_STOCK: self.stock_item_count,
            DetailInfo.TOTAL_IN_STOCK: self.total_in_stock,
        }

    # use DetailInfo consts as names
    def get_detail(self, name: str):
        return self.details.get(name)
