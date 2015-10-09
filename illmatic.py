import uuid
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from sqlalchemy.dialects.postgresql import UUID

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://illmatic:zaq123@localhost/illmatic'
db = flask.ext.sqlalchemy.SQLAlchemy(app)


interface_slaves = db.Table('interface_slaves',
    db.Column('parent', UUID(as_uuid=True),
        db.ForeignKey('interface.id', ondelete='CASCADE')),
    db.Column('slave', UUID(as_uuid=True), db.ForeignKey('interface.id',
        ondelete='CASCADE'))
)

class Interface(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Unicode(128))
    vlan = db.Column(db.Integer)
    node_id = db.Column(db.Unicode)
    if_type = db.Column(db.Unicode)
    slaves = db.relationship('Interface',
            secondary='interface_slaves',
            primaryjoin="interface.c.id==interface_slaves.c.parent",
            secondaryjoin="interface.c.id==interface_slaves.c.slave",
            backref='parent_iface'
    )
    provider = db.Column(db.Unicode(25))


#class Bond(db.Model):
#    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#    name = db.Column(db.Unicode(32))
#    slave_ifs = db.relationship('Interface', backref='bond')
    
#class Port(db.Model):
#    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#    bridge_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bridge.id'))
#    interface_id = db.Column(UUID(as_uuid=True), db.ForeignKey('interface.id'))
#    bond_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bond.id'))
     

#class Bridge(db.Model):
#    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#    name = db.Column(db.Unicode)
#    provider = db.Column(db.Unicode(25))


class IPAddress(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interface_id = db.Column(UUID(as_uuid=True), db.ForeignKey('interface.id',
                                                     ondelete='CASCADE'))
    ip_range_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ip_range.id',
                                                     ondelete='CASCADE'))
    address = db.Column(db.Unicode(25), nullable=False)
    meta = db.Column(db.Text)


class IPRange(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('network.id'))
    first = db.Column(db.Unicode(25), nullable=False)
    last = db.Column(db.Unicode(25), nullable=False)


class Network(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Unicode(50), nullable=False)
    cidr = db.Column(db.Unicode(25))
    gateway = db.Column(db.Unicode(25))
    ip_ranges = db.relationship('IPRange', backref='network',
        cascade='all, delete')
    meta = db.Column(db.Text)
    

db.drop_all()
db.create_all()

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Interface, methods=['GET', 'POST', 'PUT', 'DELETE'])
#manager.create_api(Bond, methods=['GET', 'POST', 'PUT', 'DELETE'])
#manager.create_api(Port, methods=['GET', 'POST', 'PUT', 'DELETE'])
#manager.create_api(Bridge, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(IPAddress, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(IPRange, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Network, methods=['GET', 'POST', 'PUT', 'DELETE'])

app.run()
