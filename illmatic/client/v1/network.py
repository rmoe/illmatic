from illmatic.client.base import BaseManager
from illmatic.client.base import BaseResource


class Network(BaseResource):
    def delete(self):
        return self.manager.delete(self)


class NetworkManager(BaseManager):
    
    model = Network

    def __init__(self, client):
        super(NetworkManager, self).__init__(client)

    def get(self, network_id):
        return self._get('/networks/{0}'.format(network_id))

    def list(self):
        return self._list('/networks')

    def update(self, network, **kwargs):
        return self._put('/networks/{0}'.format(network.id), kwargs)

    def delete(self, network):
        return self._delete('/networks/{0}'.format(network.id))

    def create(self, name, cidr=None, gateway=None, vlan=None, meta=None):

        data = {
            'name': name,
            'cidr': cidr,
            'gateway': gateway,
            'vlan': vlan,
            'meta': meta
        }
        return self._post('/networks/', data)
