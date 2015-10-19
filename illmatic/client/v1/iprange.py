from illmatic.client.base import BaseManager
from illmatic.client.base import BaseResource

class IPRange(BaseResource):
    def delete(self):
        return self.manager.delete(self)


class IPRangeManager(BaseManager):
    
    model = IPRange

    def __init__(self, client):
        super(IPRangeManager, self).__init__(client)

    def get(self, ip_range_id):
        return self._get('/ipranges/{0}'.format(network_id))

    def list(self):
        return self._list('/ipranges')

    def update(self, network, **kwargs):
        return self._put('/ipranges/{0}'.format(network.id), kwargs)

    def delete(self, network):
        return self._delete('/ipranges/{0}'.format(network.id))

    def create(self, first, last, network=None):

        data = {
            'network_id': network.id,
            'first': first,
            'last': last,
        }
        return self._post('/ipranges/', data)
