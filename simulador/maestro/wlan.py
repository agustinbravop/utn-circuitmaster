# import network
import asyncio
import binascii


async def connect_to_wifi(ssid: str, password: str, max_retries=3):
    """Conecta el dispositivo a Wifi. Devuelve la dirección IP y la máscara de subred."""
    # Configurar el WiFi en modo cliente (station)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    mac_address = binascii.hexlify(
        network.WLAN().config("mac"), ":").decode()
    print(f"MAC: {mac_address}")

    retries = 0
    print(f"Conectando a WiFi...", end="")
    while not wlan.isconnected() and retries < max_retries:
        print(".", end="")
        wlan.connect(ssid, password)
        retries += 1
        await asyncio.sleep(2)  # Esperar antes del próximo intento

    print()  # Termina la cadena de puntos suspensivos
    if wlan.isconnected():
        return wlan.ifconfig()
    else:
        return None
