from pecan import expose, redirect
from webob.exc import status_map
from illmatic.model.models import Interface
from illmatic.model.models import IPAddress
from illmatic.model.models import IPRange
from illmatic.model.models import Network
from illmatic.model.models import Route
from illmatic.controllers.base import BaseController


class NetworkController(BaseController):

    model = Network


class InterfaceController(BaseController):

    model = Interface


class IPAddressController(BaseController):

    model = IPAddress


class IPRangeController(BaseController):

    model = IPRange


class RouteController(BaseController):

    model = Route

class RootController(object):

    networks = NetworkController()
    interfaces = InterfaceController()
    ipranges = IPRangeController()
    ipaddresses = IPAddressController()
    routes = RouteController()
