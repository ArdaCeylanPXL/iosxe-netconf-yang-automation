from ncclient import manager
from xml.dom import minidom
import sys

ROUTER = {
    "host": "10.176.163.50",
    "port": 830,
    "username": "cisco",
    "password": "cisco"
}

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
        look_for_keys=False,
        timeout=30
    ) as m:

        print("NETCONF session established\n")

        print("Retrieving server capabilities...\n")

        capabilities = list(m.server_capabilities)

        for capability in capabilities:
            print(capability)

        print("\nOpening XML configuration file...\n")

        with open("../configs/router_config.xml") as f:
            config_data = f.read()

        print("Sending configuration...\n")

        response = m.edit_config(
            target="running",
            config=config_data,
            default_operation="merge"
        )

        print("\nNETCONF Reply:\n")

        xml_pretty = minidom.parseString(
            response.xml
        ).toprettyxml()

        print(xml_pretty)

        print("Validating deployment...\n")

        running_config = m.get_config(source='running').data_xml

        if "NETCONF-R1" in running_config:
            print("Validation successful: hostname detected.\n")
        else:
            print("Validation failed: hostname not found.\n")

        print("DEPLOYMENT SUCCESSFUL!")

except Exception as e:

    print("\nERROR DETECTED\n")
    print(e)
    sys.exit(1)
