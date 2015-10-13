import sys
import json
import os
import random
from netaddr import IPRange

NAILGUN_PATH=None
assert NAILGUN_PATH, "Set NAILGUN_PATH to nailgun directory"
sys.path.insert(0, NAILGUN_PATH)

from illmatic.db import db
from illmatic.db import models
from nailgun.db import db as ndb
from nailgun.db.sqlalchemy import models as nmodels

def rand_mac():
 return "52:54:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        )

def import_stuff():
    ranges = {}
    for network in ndb().query(nmodels.NetworkGroup).all():
        inet = models.Network(
            name=network.name,
            cidr=network.cidr,
            gateway=network.gateway,
            vlan=network.vlan_start,
            meta=json.dumps(network.meta)
        )
        db().add(inet)
        db().commit()

        for ipr in network.ip_ranges:
            new_ipr = models.IPRange(
                network_id=inet.id,
                first=ipr.first,
                last=ipr.last
            )
            db().add(new_ipr)
            db().commit()

            ranges[str(new_ipr.id)] = IPRange(ipr.first, ipr.last)


    slaves = {}
    for iface in ndb().query(nmodels.NodeNICInterface).all():
        new_iface = models.Interface(
            name=iface.name,
            mac=iface.mac,
            node_id=iface.node_id,
            if_type='ether',
            interface_properties=json.dumps(iface.interface_properties),
            driver=iface.driver,
            bus_info=iface.bus_info,
            offloading_modes=json.dumps(iface.offloading_modes),
            provider='linux'
        )
        db().add(new_iface)
        db().commit()
        if iface.parent_id:
            slaves.setdefault(iface.parent_id, [])
            slaves[iface.parent_id].append(new_iface)

    for iface in ndb().query(nmodels.NodeBondInterface).all():
        slave_ifs = slaves[iface.id]
        new_iface = models.Interface(
            name=iface.name,
            mac=rand_mac(),
            node_id=iface.node_id,
            if_type='bond',
            interface_properties=json.dumps(iface.bond_properties),
            provider='linux',
            slaves=slave_ifs
        )

    for ip in ndb().query(nmodels.IPAddr).all():
        iface = None
        meta = ''
        ipr_id = None

        interface_id = None
        if ip.node:
            for i in ip.node_data.interfaces + ip.node_data.bond_interfaces:
                if ip.network in [n['id'] for n in i.assigned_networks]:
                    interface_id = \
                    db().query(models.Interface).filter_by(node_id=str(ip.node),
                            name=i.name).first().id

        if ip.vip_type:
            meta = 'vip_type={0}'.format(ip.vip_type)

        for range_id, ipr in ranges.items():
            if ip.ip_addr in ipr:
                ipr_id=range_id
                break

        new_ip = models.IPAddress(
            interface_id=interface_id,
            ip_range_id=ipr_id,
            address=ip.ip_addr,
            meta=meta
        )
        db().add(new_ip)
    db().commit()

if __name__ == "__main__":
    import_stuff()
