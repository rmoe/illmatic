import flask
import flask.ext.restless
from illmatic.db import db
from illmatic.db import init_db, drop_db
from illmatic.db.models import Interface, IPAddress, IPRange, Network

app = flask.Flask(__name__)
app.config['DEBUG'] = True

drop_db()
init_db()

manager = flask.ext.restless.APIManager(app, session=db())

manager.create_api(Interface, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(IPAddress, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(IPRange, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Network, methods=['GET', 'POST', 'PUT', 'DELETE'])

app.run()
