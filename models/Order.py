import os
from dotenv import load_dotenv
from helpers import RequestHandler


class Order(RequestHandler):

    def __init__(self, isin: str = "", valid_until: float = 0, quantity: int = 0, side: str = "",
                 stop_price: float = 0, limit_price: float = 0, uuid: str = ""):
        self.isin = isin
        self.valid_until = valid_until
        self.quantity = quantity
        self.side = side
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.uuid = uuid

    def place_order(self):
        order_details = {
            "isin": self.isin,  # set ISIN
            "valid_until": self.valid_until,  # specify your timestamp
            "side": self.side,  # set side
            "quantity": self.quantity,  # set quantity
        }
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/'
        response = self.post_data(endpoint, order_details)
        return response

    def get_orders(self):
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/'
        response = self.get_data_trading(endpoint)
        return response

    def activate_order(self, order_uuid):
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/{order_uuid}/activate/'
        response = self.put_data(endpoint)
        return response
