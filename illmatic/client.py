import json
import netaddr
import requests

base_url = 'http://127.0.0.1:5000/api/{0}'
base_headers = {'Content-Type': 'application/json'}


class Base(object):

    @classmethod
    def POST(cls, data, headers=base_headers):
        response = requests.post(cls.url, data=json.dumps(data),
                                 headers=headers)

        return response.json()

    @classmethod
    def PUT(cls, instance_id, data, headers=base_headers):
        url = '{0}/{1}'.format(cls.url, instance_id)
        response = requests.put(url, data=json.dumps(data), headers=headers)

        return response.json()

    @classmethod
    def DELETE(cls, instance_id, headers=base_headers):
        url = '{0}/{1}'.format(cls.url, instance_id)
        response = requests.delete(url, headers=headers)

        return response.json()

    @classmethod
    def GET(cls, filters=None, headers=base_headers):
        url = cls.url
        if filters:
            url = '{0}?q={{"filters":{1}}}'.format(url, filters)

        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def delete(cls, obj_id):
        return cls.DELETE(obj_id)

class Interface(Base):

    url = base_url.format('interface')

    @classmethod
    def create(cls, name, mac, node_id, provider='linux', slaves=[], if_type='ether'):
        data = {
            'name': name,
            'mac': mac,
            'node_id': node_id,
            'slaves': slaves,
            'if_type': if_type,
            'provider': provider
        }

        return cls.POST(data)

    @classmethod
    def get_by_node(cls, node_id):
        filters = '[{{"name":"node_id", "op":"eq", "val":"{0}"}}]'.format(node_id)
        
        return cls.GET(filters)


class IPRange(Base):

    url = base_url.format('ip_range')

    @classmethod
    def create(cls, network_id, first, last):
        data = {
            'network_id': network_id,
            'first': first,
            'last': last
        }

        return cls.POST(data)


class IPAddress(Base):

    url = base_url.format('ip_address')

    @classmethod
    def assign(cls, interface_id, ip_range_id, address=None):
        data = {
            'interface_id': interface_id,
            'ip_range_id': ip_range_id,
            'address': address
        }

        return cls.POST(data)

    @classmethod
    def get_free_ip(cls, network_id):
        network = Network.get_by_id(network_id)[0]

        for ip_range in network['ip_ranges']:
            filters = '[{{"name":"ip_range_id", "op":"eq", "val":"{0}"}}]'.format(ip_range['id'])
            response = cls.GET(filters)
            addr_in_use = response['objects']

            addrs = set()
            for addr in addr_in_use:
                addrs.add(addr['address'])

            ipr = netaddr.IPRange(ip_range['first'], ip_range['last'])
            for ip_address in ipr:
                if str(ip_address) not in addrs:
                    return str(ip_address)

class Network(Base):

    url = base_url.format('network')

    @classmethod
    def create(cls, name, cidr, gateway, ip_ranges):
        data = {
            'name': name,
            'cidr': cidr,
            'gateway': gateway
        }
        response = cls.POST(data)
        net_id = response['id']

        for ip_range in ip_ranges:
            IPRange.create(net_id, *ip_range)

        return response

    @classmethod
    def get_all(cls):
        return cls.GET()

    @classmethod
    def get_by_id(cls, network_id):
        filters = '[{{"name":"id", "op":"eq", "val":"{0}"}}]'.format(network_id)
        
        net = cls.GET(filters)
        return net['objects']


if __name__ == "__main__":
    if1 = Interface.create('eth0', 1).json()
    if2 = Interface.create('eth1', 1).json()

    b = Bond.create('bond0', [if1, if2], 1).json()
    ng1 = Network.create('net1', '10.20.0.0/24', '10.20.0.1',
            [('10.20.0.10', '10.20.0.20'),
             ('10.20.0.40', '10.20.0.50')]).json()

    br_ex = Bridge.create('br-ex', [b], 12, 1)
