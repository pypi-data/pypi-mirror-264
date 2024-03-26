"""Ithaca SDK."""
import requests
from eth_account import Account

from .analytics import Analytics
from .auth import Auth
from .calculation import Calculation
from .client import Client
from .constants import ENVS
from .fundlock import Fundlock
from .market import Market
from .orders import Orders  # type: ignore  # noqa: F401
from .protocol import Protocol
from .socket import Socket


class IthacaSDK:
    """Ithaca SDK."""

    def __init__(self, private_key, env_name="SALT"):
        """Class constructor."""
        self.env = ENVS.get(env_name)
        self.account = Account.from_key(private_key)
        self.session = requests.Session()
        self.base_url = self.env.get("base_url")
        self.subgraph_url = self.env.get("subgraph")
        self.ws_url = self.env.get("ws_url")
        self.rpc_url = self.env.get("rpc_url")

        self.auth = Auth(self)
        self.protocol = Protocol(self)
        self.market = Market(self)
        self.client = Client(self)
        self.orders = Orders(self)
        self.calculation = Calculation(self)
        self.socket = Socket(self)
        self.fundlock = Fundlock(self)
        self.analytics = Analytics(self)

    def post(self, endpoint, json=None):
        """Make Post Request.

        Args:
            endpoint (_type_): _description_
            json (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        verify = False if "localhost" in self.base_url else True
        res = self.session.post(self.base_url + endpoint, json=json, verify=verify)
        try:
            return res.json()
        except requests.JSONDecodeError:
            return res

    def get(self, endpoint):
        """Make GET request.

        Args:
            endpoint (_type_): _description_

        Returns:
            _type_: _description_
        """
        headers = {"Content type": "application/json"}
        verify = True if self.base_url.startswith("https") else False
        res = self.session.get(self.base_url + endpoint, params=headers, verify=verify)
        return res.json()
