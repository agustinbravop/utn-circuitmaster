from http_server import run_http_server
from network_discovery import calculate_broadcast, discover_terminals
from wlan import connect_to_wifi
from terminals import poll_terminal_data
import asyncio
import sys
import netifaces as ni


# Datos para conectarse a la red WiFi
# WLAN_SSID = sys.argv[1]
# WLAN_PASSWORD = sys.argv[2]

# Datos para las interfaces del maestro
BROADCAST_PORT = int(sys.argv[1])
HTTP_SERVER_PORT = int(sys.argv[2])
print(sys.argv)


async def master_monitoring():
    print("Controlador maestro")

    print(f"Conectando a WiFi...")
    # if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    # if if_config is None:
    #     print("Error al conectar a la red Wifi.")
    #     return None

    # ip_address, subnet_mask, _, _ = if_config
    interface = ni.gateways()['default'][ni.AF_INET][1]
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]

    ip_address = addr['addr']
    subnet_mask = addr['netmask']
    print(f"Conectado! IP: {ip_address}, Máscara de subred: {subnet_mask}")

    broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
    print("Dirección de broadcast:", broadcast_ip)

    await asyncio.gather(
        run_http_server(ip_address, HTTP_SERVER_PORT),
        discover_terminals(broadcast_ip, BROADCAST_PORT),
        poll_terminal_data(),
    )

asyncio.run(master_monitoring())
