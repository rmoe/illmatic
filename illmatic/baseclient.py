import requests
from oslo_serialization import jsonutils


class BaseClient(object):

    base_url = 'http://127.0.0.1:8080'

    def request(self, url, method, **kwargs):
        url = '{0}{1}'.format(self.base_url, url)
        resp = requests.request(method, url, **kwargs)

        try:
            body = jsonutils.loads(resp.text)
        except (ValueError, TypeError):
            body = None

        return resp, body

    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)
