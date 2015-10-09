import json
import requests

base_url = 'http://127.0.0.1:5000/api/{0}'
base_headers = {'Content-Type': 'application/json'}


def get_interfaces():
    url = base_url.format('interface')

class Base(object):

    @classmethod
    def POST(cls, data, headers=base_headers):
        response = requests.post(cls.url, data=json.dumps(data),
                                 headers=headers)

        return response

    @classmethod
    def PUT(cls, instance_id, data, headers=base_headers):
        url = '{0}/{1}'.format(cls.url, instance_id)
        response = requests.put(url, data=json.dumps(data), headers=headers)

        return response

    @classmethod
    def DELETE(cls, instance_id, headers=base_headers):
        url = '{0}/{1}'.format(cls.url, instance_id)
        response = requests.delete(url, headers=headers)

        return response

    @classmethod
    def delete(cls, obj_id):
        return cls.DELETE(obj_id)

class Interface(Base):

    url = base_url.format('interface')

    @classmethod
    def create(cls, name, vlan, node_id, slaves=[], if_type='ether'):
        data = {
            'name': name,
            'vlan': vlan,
            'node_id': node_id,
            'slaves': slaves,
            'if_type': if_type,
        }

        return cls.POST(data)


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
        net_id = response.json()['id']

        for ip_range in ip_ranges:
            IPRange.create(net_id, *ip_range)

        return response

class Bridge(Base):

    url = base_url.format('bridge')

    @classmethod
    def create(cls, name, interfaces, vlan, node_id):
        br = Interface.create(name, vlan, node_id, slaves=interfaces,
                              if_type='bridge')

        return br.json()

class Port(Base):

    url = base_url.format('port')

    @classmethod
    def create(cls, bridge, interface=None, bond=None):
        data = {
            'bridge_id': bridge,
            'interface': interface,
            'bond': bond
        }

        return cls.POST(data)

class Bond(object):

    @classmethod
    def create(cls, name, interfaces, vlan, node_id):
        bond = Interface.create(name, vlan, node_id, slaves=interfaces,
                                if_type='bond')

        return bond


if __name__ == "__main__":
    if1 = Interface.create('eth0', '12', 1).json()
    if2 = Interface.create('eth1', '12', 1).json()

    b = Bond.create('bond0', [if1, if2], 12, 1).json()
    ng1 = Network.create('net1', '10.20.0.0/24', '10.20.0.1',
            [('10.20.0.10', '10.20.0.20'),
             ('10.20.0.40', '10.20.0.50')]).json()

    br_ex = Bridge.create('br-ex', [b], 12, 1)
    #Port.create(br_ex['id'], if1['id'])
    #Port.create(br_ex['id'], if2['id'])
