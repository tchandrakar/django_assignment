import json
from json import JSONEncoder
from .models import SellerToken

class SellerTokenEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
