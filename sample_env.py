import client
import random
import uuid

def rand_mac():
 return "52:54:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        )

def discover_node(iface_count=4):
    node_id = uuid.uuid4()
    for iface in range(iface_count):
        client.Interface.create(
            name='eth{0}'.format(iface),
            mac=rand_mac(),
            provider='linux',
            node_id=str(node_id)
        )
    return node_id


def add_networks():
    client.Network.create(
        name='public',
        cidr='10.21.0.0/24',
        gateway='10.21.0.1',
        ip_ranges=[('10.21.0.2', '10.21.0.10'),
                    ('10.21.0.100', '10.21.0.110')]
    )
    client.Network.create(
        name='storage',
        cidr='10.22.0.0/24',
        gateway=None,
        ip_ranges=[('10.22.0.1', '10.22.0.254')]
    )
    client.Network.create(
        name='management',
        cidr='10.23.0.0/24',
        gateway='10.23.0.1',
        ip_ranges=[('10.23.0.2', '10.23.0.254')]
    )
    client.Network.create(
        name='private',
        cidr='10.24.0.0/24',
        gateway='10.24.0.1',
        ip_ranges=[('10.24.0.2', '10.24.0.254')]
    )

def assign_ips(nodes):
    for node in nodes:
        interfaces = (i for i in client.Interface.get_by_node(node)['objects'])

        for network in client.Network.get_all()['objects']:
            interface = next(interfaces)

            ip_range = network['ip_ranges'][0]
            address = client.IPAddress.get_free_ip(network['id'])
            client.IPAddress.assign(interface['id'], ip_range['id'], address)


def create_env():
    nodes = []
    for i in range(4):
        nodes.append(discover_node())

    add_networks()
    assign_ips(nodes)
    
if __name__ == "__main__":
    create_env()
