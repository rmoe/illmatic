import uuid

from illmatic.model import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy import types
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql as psql


interface_slaves = Table(
    'interface_slaves',
    Base.metadata,
    Column('parent', String(64),
           ForeignKey('interface.id', ondelete='CASCADE')),
    Column('slave', String(64),
           ForeignKey('interface.id', ondelete='CASCADE'))
)


class Interface(Base):
    __tablename__ = 'interface'

    id = Column(String(64), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(Unicode(128))
    mac = Column(Unicode(17), nullable=False)
    node_id = Column(Unicode)
    if_type = Column(Unicode)
    slaves = relationship(
        'Interface',
        secondary='interface_slaves',
        primaryjoin="interface.c.id==interface_slaves.c.parent",
        secondaryjoin="interface.c.id==interface_slaves.c.slave",
        backref='parent_iface'
    )
    interface_properties = Column(Text)
    current_speed = Column(Integer)
    max_speed = Column(Integer)
    driver = Column(Text)
    bus_info = Column(Text)
    pxe = Column(Boolean)
    offloading_modes = Column(Text)
    provider = Column(Unicode(25))


class IPAddress(Base):
    __tablename__ = 'ip_address'

    id = Column(String(64), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    interface_id = Column(String(64), ForeignKey('interface.id',
                                                 ondelete='CASCADE'))
    ip_range_id = Column(String(64), ForeignKey('ip_range.id',
                                                ondelete='CASCADE'))
    address = Column(Unicode(25), nullable=False)
    meta = Column(Text)


class IPRange(Base):
    __tablename__ = 'ip_range'
    __fields__ = ('id', 'network_id', 'first', 'last')

    id = Column(String(64), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    network_id = Column(String(64), ForeignKey('network.id'))
    first = Column(Unicode(25), nullable=False)
    last = Column(Unicode(25), nullable=False)

    def __json__(self):
        output = {}
        for field in self.__fields__:
            output[field] = getattr(self, field)

        return output


class Network(Base):
    __tablename__ = 'network'
    __fields__ = ('id', 'name', 'cidr', 'gateway', 'vlan', 'meta')

    id = Column(String(64), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(Unicode(50), nullable=False)
    cidr = Column(Unicode(25))
    gateway = Column(Unicode(25))
    vlan = Column(Integer)
    ip_ranges = relationship('IPRange', backref='network',
                             cascade='all, delete')
    meta = Column(Text)

    def __json__(self):
        output = {}
        for field in self.__fields__:
            output[field] = getattr(self, field)
        output['id'] = str(output['id'])

        output['ip_ranges'] = []
        for ip_range in self.ip_ranges:
            output['ip_ranges'].append(ip_range.__json__())

        return output


class Route(Base):
    __tablename__ = 'routes'

    id = Column(String(64), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(String(64))
    nexthop = Column(String(64))
    netmask = Column(String(64))
    default = Column(Boolean)
    metric = Column(Integer)
    interface_id = Column(String(64), ForeignKey('interface.id',
                                                 ondelete='CASCADE'))
