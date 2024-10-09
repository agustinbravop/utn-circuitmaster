import wifi
import asyncio
import binascii


async def connect_to_wifi(ssid: str, password: str):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    mac_address = binascii.hexlify(wifi.radio.mac_address, ":").decode()
    print(f"MAC: {mac_address}")

    print(f"Conectando a WiFi...")

    try:
        wifi.radio.connect(ssid, password)
    except Exception as e:
        print(f"Error al conectarse a Wifi. Reinicie el dispositivo. Error: {e}")

    if wifi.radio.connected:
        return str(wifi.radio.ipv4_address), str(wifi.radio.ipv4_subnet)
    else:
        return None
