from illmatic.client.base import BaseManager
from illmatic.client.base import BaseResource


class Interface(BaseResource):
    def delete(self):
        return self.manager.delete(self)


class InterfaceManager(BaseManager):

    model = Interface

    def __init__(self, client):
        super(InterfaceManager, self).__init__(client)

    def list(self):
        return self._list('/interfaces')

    def get(self, interface_id):
        return self._get('/interfaces/{0}'.format(interface_id))

    def delete(self, interface):
        return self._delete('/interfaces/{0}'.format(interface.id))

    def update(self, interface, **kwargs):
        return self._put('/interfaces/{0}'.format(interface.id), kwargs)

    def create(self, name, mac, node_id=None, slaves=None,
            interface_properties=None, if_type='ether', driver=None,
            bus_info=None, offloading_modes=None, current_speed=None,
            max_speed=None, pxe=None, provider='linux'):
        
        params = {"name": name,
                  "mac": mac,
                  "node_id": node_id,
                  "slaves": slaves,
                  "interface_properties": interface_properties,
                  "if_type": if_type,
                  "driver": driver,
                  "bus_info": bus_info,
                  "offloading_modes": offloading_modes,
                  "current_speed": current_speed,
                  "max_speed": max_speed,
                  "provider": provider
                  }
        return self._post('/interfaces/', params)

    def filter(self, **kwargs):
        return self._get('/interfaces/filter/', kwargs)
