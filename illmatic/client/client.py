from illmatic.baseclient import BaseClient
from illmatic.client.v1.ipaddress import IPAddressManager
from illmatic.client.v1.iprange import IPRangeManager
from illmatic.client.v1.network import NetworkManager
from illmatic.client.v1.interface import InterfaceManager


class Client(BaseClient):

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.networks = NetworkManager(self)
        self.ip_ranges = IPRangeManager(self)
        self.interfaces = InterfaceManager(self)
        self.ip_addresses = IPAddressManager(self)
