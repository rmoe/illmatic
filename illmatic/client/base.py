from illmatic.openstack.common.apiclient import base

class BaseResource(base.Resource):
    "Base class for resources (interface, network, etc.)"

class BaseManager(object):
    
    model = None

    def __init__(self, client):
        super(BaseManager, self).__init__()
        self.client = client

    def _list(self, url, obj_class=None):
        resp, body = self.client.get(url)

        if obj_class is None:
            obj_class = self.model

        return [obj_class(self, res, loaded=True) for res in body if res]

    def _get(self, url, params=None):
        resp, body = self.client.get(url, params=params)

        if isinstance(body, list):
            return [self.model(self, b, loaded=True) for b in body]

        return self.model(self, body, loaded=True)

    def _post(self, url, body=None):
        resp, body = self.client.post(url, data=body)

        return self.model(self, body)

    def _put(self, url, body=None):
        resp, body = self.client.put(url, data=body)

        return self.model(self, body)

    def _delete(self, url):
        return self.client.delete(url)
