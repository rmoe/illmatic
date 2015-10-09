
To start the API server:
```
python illmatic.py
```

Server will listen on localhost:5000

Sample API output from api/interfaces. Shows two interfaces bonded together
and that bond added to a bridge.
```
{
  "num_results": 4,
  "objects": [
    {
      "id": "627d3cc0-efd6-414e-acbe-9e182aae95ba",
      "if_type": "ether",
      "name": "eth0",
      "node_id": "1",
      "parent_iface": [
        {
          "id": "d332fec2-f7fd-4355-934d-452450d053c1",
          "if_type": "bond",
          "name": "bond0",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        }
      ],
      "provider": null,
      "slaves": [],
      "vlan": 12
    },
    {
      "id": "9ed76388-cff9-4e39-9e64-a488044e05fb",
      "if_type": "bridge",
      "name": "br-ex",
      "node_id": "1",
      "parent_iface": [],
      "provider": null,
      "slaves": [
        {
          "id": "d332fec2-f7fd-4355-934d-452450d053c1",
          "if_type": "bond",
          "name": "bond0",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        }
      ],
      "vlan": 12
    },
    {
      "id": "d332fec2-f7fd-4355-934d-452450d053c1",
      "if_type": "bond",
      "name": "bond0",
      "node_id": "1",
      "parent_iface": [
        {
          "id": "9ed76388-cff9-4e39-9e64-a488044e05fb",
          "if_type": "bridge",
          "name": "br-ex",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        }
      ],
      "provider": null,
      "slaves": [
        {
          "id": "627d3cc0-efd6-414e-acbe-9e182aae95ba",
          "if_type": "ether",
          "name": "eth0",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        },
        {
          "id": "d6200046-aff1-40cf-93a1-8fae04a65751",
          "if_type": "ether",
          "name": "eth1",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        }
      ],
      "vlan": 12
    },
    {
      "id": "d6200046-aff1-40cf-93a1-8fae04a65751",
      "if_type": "ether",
      "name": "eth1",
      "node_id": "1",
      "parent_iface": [
        {
          "id": "d332fec2-f7fd-4355-934d-452450d053c1",
          "if_type": "bond",
          "name": "bond0",
          "node_id": "1",
          "provider": null,
          "vlan": 12
        }
      ],
      "provider": null,
      "slaves": [],
      "vlan": 12
    }
  ],
  "page": 1,
  "total_pages": 1
}
```
