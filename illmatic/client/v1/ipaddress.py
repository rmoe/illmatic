from illmatic.client.base import BaseManager
from illmatic.client.base import BaseResource


class IPAddress(BaseResource):
    def delete(self):
        return self.manager.delete(self)


class IPAddressManager(BaseManager):

    model = IPAddress

    def __init__(self, client):
        super(IPAddressManager, self).__init__(client)

    def list(self):
        return self._list('/ipaddresses')

    def get(self, ip_address_id):
        return self._get('/ipaddresses/{0}'.format(ip_address_id))

    def delete(self, ip_address):
        return self._delete('/ipaddresses/{0}'.format(ip_address.id))

    def update(self, ip_address, **kwargs):
        return self._put('/ipaddresses/{0}'.format(ip_address.id), kwargs)

    def create(self, address, interface_id=None, ip_range_id=None, meta=None):
        
        params = {'address': address,
                  'interface_id': interface_id,
                  'ip_range_id': ip_range_id,
                  'meta': meta
                  }
        return self._post('/ipaddresses/', params)
