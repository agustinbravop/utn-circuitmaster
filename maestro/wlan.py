import wifi
import asyncio
import binascii


async def connect_to_wifi(ssid: str, password: str, max_retries=3):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    mac_address = binascii.hexlify(wifi.radio.mac_address, ":").decode()
    print(f"MAC: {mac_address}")

    retries = 0
    print(f"Conectando a WiFi...", end="")

    while retries < max_retries:

        try:
            wifi.radio.connect(ssid, password)
            retries = max_retries
        except Exception as e:
            print(".", e, end="")
            retries += 1
            await asyncio.sleep(1)  # Esperar antes del próximo intento

    print()  # Termina la cadena de puntos suspensivos
    if wifi.radio.connected:
        return str(wifi.radio.ipv4_address), str(wifi.radio.ipv4_subnet)
    else:
        return None
