from lbank.api import HttpClient
from lbank.spot._base_data import BaseData
from lbank.spot._account import Account
from lbank.spot._order import Order
from lbank.spot._withdraw import Withdraw
from lbank.spot._wallet import Wallet
from lbank.spot._market import Market
from lbank.spot._trade import Trade


class Spot(
        HttpClient, BaseData, Account, Order, Withdraw, Wallet, Market, Trade):
    def __init__(
            self, sign_method: str = "RSA", api_key: str = None,
            api_secret: str = None, private_key: str = None,
            base_url: str = "https://api.lbkex.com/v2"):
        HttpClient.__init__(
            sign_method, api_key, api_secret, private_key, base_url)
