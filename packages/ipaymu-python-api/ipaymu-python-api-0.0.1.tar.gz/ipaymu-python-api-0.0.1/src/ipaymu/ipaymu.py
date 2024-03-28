from curl import request
import numpy as np


class Config:
    """
    Ipaymu Configuration Constructor

    Parameters:
        prod (bool) -> App environment
    """

    def __init__(self, prod: bool):
        self.prod = prod

        if prod:
            base = "https://my.ipaymu.com/api/v2"
        else:
            base = "https://sandbox.ipaymu.com/api/v2"

        """
        General API
        """
        self.balance = base + "/balance"
        self.transaction = base + "/transaction"
        self.history = base + "/history"
        self.banklist = base + "/banklist"

        """ 
        Payment API
        """
        self.redirectpayment = base + "/payment"
        self.directpayment = base + "/payment/direct"

        """
        COD Payment
        """
        self.codarea = base + "/cod/getarea"
        self.codrate = base + "/cod/getrate"
        self.codpickup = base + "/cod/pickup"
        self.codpayment = base + "/payment/cod"

        """
        COD Tracking
        """
        self.codawb = base + "/cod/getawb"
        self.codtracking = base + "/cod/tracking"
        self.codhistory = base + "/cod/history"


class Main:
    def __init__(self, api_key=None, va=None, prod: bool = False):
        """Ipaymu Core Process

        Args:
            apiKey (Any, optional): Ipaymu API KEY. Defaults to None.
            va (Any, optional): Ipaymu Virtual Account. Defaults to None.
            prod (Any, optional): App Environment. Defaults to False.
        """
        self.config = Config(prod)
        self.api_key = api_key
        self.va = va
        self.carts = list()

        self.ureturn = None
        self.ucancel = None
        self.unotify = None
        self.name = None
        self.phone = None
        self.email = None
        self.pickup_area = None
        self.pickup_address = None
        self.delivery_area = None
        self.delivery_address = None

    def set_amount(self, amount):
        self.amount = amount

    def set_expired(self, expired):
        self.expired = expired

    def set_url(self, url: dict):
        self.ureturn = url.get("ureturn")
        self.ucancel = url.get("ucancel")
        self.unotify = url.get("unotify")

    def set_buyer(self, buyer: dict):
        self.name = buyer.get("name")
        self.phone = buyer.get("phone")
        self.email = buyer.get("email")

    def set_cod(self, data: dict):
        self.pickup_area = data.get("pickup_area")
        self.pickup_address = data.get("pickup_address")
        self.delivery_area = data.get("delivery_area")
        self.delivery_address = data.get("delivery_address")

    def set_comment(self, comments: str):
        self.comments = comments

    def add_cart(self, cart):
        self.carts = cart

    def remove(self, id):
        for index, cart in enumerate(self.carts):
            if cart["id"] == id:
                self.carts.remove(self.carts[index])

    def build_carts(self):
        length = np.array(self.carts.get("length"), dtype='str')
        width = np.array(self.carts.get("width"), dtype='str')
        height = np.array(self.carts.get("height"), dtype='str')
        
        dimension = []
        for dimension_type in np.stack((length, width, height), axis=1):
            dimension.append(":".join(type for type in dimension_type))
        
        return {
            "product": self.carts.get("product"),
            "price": self.carts.get("price"),
            "quantity": self.carts.get("quantity"),
            "description": self.carts.get("description"),
            "weight": self.carts.get("weight"),
            "dimension": dimension,
        }

    def set_api_key(self, api_key: None):
        if api_key == None:
            raise Exception

        self.api_key = api_key

    def set_va(self, va: None):
        if va == None:
            raise Exception

        self.va = va

    def history_transaction(self, data):
        return request(
            self.config.history,
            data,
            {
                "va": self.va,
                "api_key": self.api_key,
            },
        ).text

    def check_balance(self):
        return request(
            self.config.balance,
            {
                "account": self.va,
            },
            {
                "va": self.va,
                "api_key": self.api_key,
            },
        ).text

    def check_transaction(self, id):
        return request(
            self.config.history,
            {"transactionId": id},
            {
                "va": self.va,
                "api_key": self.api_key,
            },
        ).text

    def redirect_payment(self, data: dict):
        current_carts = self.build_carts()

        return request(
            self.config.redirectpayment,
            {
                "account": self.va,
                "product": current_carts.get("product"),
                "qty": current_carts.get("quantity"),
                "price": current_carts.get("price"),
                "description": current_carts.get("description"),
                "notifyUrl": self.unotify,
                "returnUrl": self.ureturn,
                "cancelUrl": self.ucancel,
                "weight": current_carts.get("weight"),
                "dimension": current_carts.get("dimension"),
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "pickupArea": self.pickup_area,
                "pickupAddress": self.pickup_address,
                "buyerName": self.name,
                "buyerEmail": self.email,
                "buyerPhone": self.phone,
                "referenceId": data.get("reference_id"),
            },
            {
                "va": self.va,
                "api_key": self.api_key,
            },
        ).text

    def direct_payment(self, data: dict):
        current_carts = self.build_carts()
        expired = data.get("expired") if data.get("expired") is not None else 1
        expired_type = (
            data.get("expired_type") if data.get("expired_type") is not None else "days"
        )

        return request(
            self.config.redirectpayment,
            {
                "account": self.va,
                "product": current_carts.get("product"),
                "qty": current_carts.get("quantity"),
                "price": current_carts.get("price"),
                "description": current_carts.get("description"),
                "notifyUrl": self.unotify,
                "returnUrl": self.ureturn,
                "cancelUrl": self.ucancel,
                "weight": current_carts.get("weight"),
                "dimension": current_carts.get("dimension"),
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "pickupArea": self.pickup_area,
                "pickupAddress": self.pickup_address,
                "buyerName": self.name,
                "buyerEmail": self.email,
                "buyerPhone": self.phone,
                "referenceId": data.get("reference_id"),
                "amount": self.amount,
                "paymentMethod": data.get("payment_method"),
                "paymentChannel": data.get("payment_channel"),
                "length": current_carts.get("length"),
                "width": current_carts.get("width"),
                "height": current_carts.get("height"),
                "deliveryArea": self.delivery_area,
                "deliveryAddress": self.delivery_address,
                "expired": expired,
                "expiredType": expired_type,
            },
            {
                "va": self.va,
                "api_key": self.api_key,
            },
        ).text
