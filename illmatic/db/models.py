import uuid

from illmatic.db import Base
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
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql as psql


interface_slaves = Table('interface_slaves', Base.metadata,
    Column('parent',psql.UUID(as_uuid=True),
        ForeignKey('interface.id', ondelete='CASCADE')),
    Column('slave', psql.UUID(as_uuid=True),
        ForeignKey('interface.id', ondelete='CASCADE'))
)

class Interface(Base):
    __tablename__ = 'interface'

    id = Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Unicode(128))
    mac = Column(Unicode(17), nullable=False)
    node_id = Column(Unicode)
    if_type = Column(Unicode)
    slaves = relationship('Interface',
            secondary='interface_slaves',
            primaryjoin="interface.c.id==interface_slaves.c.parent",
            secondaryjoin="interface.c.id==interface_slaves.c.slave",
            backref='parent_iface'
    )
    interface_properties = Column(Text)
    driver = Column(Text)
    bus_info = Column(Text)
    offloading_modes = Column(Text)
    provider = Column(Unicode(25))


class IPAddress(Base):
    __tablename__ = 'ip_address'

    id = Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interface_id = Column(psql.UUID(as_uuid=True), ForeignKey('interface.id',
                                                     ondelete='CASCADE'))
    ip_range_id = Column(psql.UUID(as_uuid=True), ForeignKey('ip_range.id',
                                                     ondelete='CASCADE'))
    address = Column(Unicode(25), nullable=False)
    meta = Column(Text)


class IPRange(Base):
    __tablename__ = 'ip_range'

    id = Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = Column(psql.UUID(as_uuid=True), ForeignKey('network.id'))
    first = Column(Unicode(25), nullable=False)
    last = Column(Unicode(25), nullable=False)


class Network(Base):
    __tablename__ = 'network'

    id = Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Unicode(50), nullable=False)
    cidr = Column(Unicode(25))
    gateway = Column(Unicode(25))
    vlan = Column(Integer)
    ip_ranges = relationship('IPRange', backref='network',
        cascade='all, delete')
    meta = Column(Text)

