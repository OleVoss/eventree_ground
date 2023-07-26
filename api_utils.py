from inventree.api import InvenTreeAPI
import requests
from PIL import Image
import io


def get_part_fields(api: InvenTreeAPI, primary_key: int):
    fields = api.get("/part/" + str(primary_key))
    return fields


def get_stockitem_fields(api: InvenTreeAPI, primary_key: int):
    fields = api.get("/stock/" + str(primary_key))
    return fields


def get_part_img(api: InvenTreeAPI, img_path: str):
    r = requests.get(img_path, headers={"Authorization": "Token " + api.token})
    img = Image.open(io.BytesIO(r.content))
    return img
