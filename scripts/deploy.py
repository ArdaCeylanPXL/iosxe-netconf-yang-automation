from ncclient import manager
from xml.dom import minidom

ROUTER = {
    "host": "10.176.163.50",
    "port": 830,
    "username": "cisco",
    "password": "cisco"
}

with open("../configs/router_config.xml") as f:
    config_data = f.read()

try:

    print("\nConnecting to CSR1000v...\n")

    with manager.connect(
        host=ROUTER["host"],
        port=ROUTER["port"],
        username=ROUTER["username"],
        password=ROUTER["password"],
        hostkey_verify=False,
        device_params={'name': 'csr'},
        allow_agent=False,
        look_for_keys=False
    ) as m:

        print("NETCONF session established\n")

        print("Sending configuration...\n")

        response = m.edit_config(
            target="running",
            config=config_data
        )

        xml_pretty = minidom.parseString(
            response.xml
        ).toprettyxml()

        print(xml_pretty)

        print("DEPLOYMENT SUCCESSFUL!")

except Exception as e:

    print("\nERROR DETECTED\n")
    print(e)
