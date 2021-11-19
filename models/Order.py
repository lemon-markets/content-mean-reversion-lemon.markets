import os
from dotenv import load_dotenv
from helpers import RequestHandler


class Order(RequestHandler):

    def __init__(self, isin: str = "", expires_at: str = "", quantity: int = 0, side: str = "",
                 stop_price: int = 0, limit_price: int = 0, order_id: str = "", venue: str = "", space_id: str = ""):
        self.isin = isin
        self.expires_at = expires_at
        self.quantity = quantity
        self.side = side
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.venue = venue
        self.order_id = order_id
        self.space_id = space_id

    def place_order(self):
        order_details = {
            "isin": self.isin,
            "expires_at": self.expires_at,
            "side": self.side,
            "quantity": self.quantity,
            "venue": self.venue,
            "space_id": self.space_id,
        }
        load_dotenv()
        endpoint = f'orders/'
        response = self.post_data(endpoint, order_details)
        return response

    def get_orders(self):
        load_dotenv()
        space_id = os.getenv("SPACE_ID")
        endpoint = f'orders/?space_id={space_id}/'
        response = self.get_data_trading(endpoint)
        return response

    def activate_order(self, order_id):
        load_dotenv()
        endpoint = f'orders/{order_id}/activate/'
        response = self.post_data(endpoint, {})
        return response
