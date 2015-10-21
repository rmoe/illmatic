import uuid
from pecan import expose, abort, response
from webob.exc import status_map
from illmatic.model import Session as db
#from illmatic.model.models import

class BaseController(object):

    def _get_object(self, id):
        obj = db.query(self.model).get(id)
        if not obj:
            abort(404)

        return obj

    @expose(generic=True, template='json')
    def index(self):
        pass

    @index.when(method='GET', template='json')
    def on_get(self, id=None):
        if id:
            obj = self._get_object(id)
        else:
            obj = db.query(self.model).all()

        return obj

    @index.when(method='POST', template='json')
    def on_post(self, **kw):
        if 'id' not in kw:
            kw['id'] = str(uuid.uuid4())
        obj = self.model(**kw)
        db.add(obj)
        return obj

    @index.when(method='PUT', template='json')
    def on_put(self, id, **kw):
        obj = self._get_object(id)

        kw.pop('id', None)
        
        for k,v in kw.items():
            setattr(obj, k, v)

        db.add(obj)
        return obj

    @index.when(method='DELETE', template='json')
    def on_delete(self, id):
        obj = self._get_object(id)
        db.delete(obj)
        response.status = 204

    @expose(template='json')
    def filter(self, **kwargs):
        objs = db.query(self.model).filter_by(**kwargs)
        return objs.all()
