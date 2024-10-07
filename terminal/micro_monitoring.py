import network
import socket
import uasyncio as asyncio
import ubinascii as binascii
import ujson as json
import time


async def connect_to_wifi(ssid: str, password: str, max_retries=5):
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

    print()
    if wlan.isconnected():
        return wlan.ifconfig()
    else:
        return None


async def listen_for_discovery_messages(team_name: str, broadcast_port: int, tcp_port: int):
    """Esperar broadcast de descubrimiento del maestro."""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Escuchar en todas las interfaces de red
    udp.bind(("0.0.0.0", broadcast_port))
    # No bloquear la ejecución si no hay mensajes
    udp.setblocking(False)

    while True:
        try:
            msg, addr = udp.recvfrom(1024)
            if msg == b"DISCOVER":
                print("Mensaje de descubrimiento recibido de:", addr)
                response = f"TERMINAL;{team_name};{tcp_port}"
                udp.sendto(response.encode(), addr)
        except OSError:
            await asyncio.sleep(1)  # Ceder control si no hay mensajes

        await master_disconnected.wait()


async def start_tcp_server(port: int, get_app_data):
    """Iniciar un servidor TCP para que el maestro pueda conectarse."""
    server = await asyncio.start_server(await create_handler(get_app_data), "0.0.0.0", port)
    await server.wait_closed()


async def create_handler(get_app_data):
    """Construye un handler con acceso a la función para obtener datos del terminal."""

    async def handle_client(reader, writer):
        """Manejar la conexión del maestro de forma asincrónica."""
        master_disconnected.clear()
        addr = writer.get_extra_info("peername")
        print(f"Conexión establecida con {addr}")

        while True:
            try:
                data = await reader.read(1024)

                if data == b"":
                    # Mensaje de desconexión
                    break

                if data == b"GETDATA":
                    # Enviar la data del terminal
                    response = json.dumps(get_app_data())
                    writer.write(response.encode())
                    await writer.drain()

            except OSError as e:
                print(f"Error en la conexión: {e}")

        writer.close()
        await writer.wait_closed()
        master_disconnected.set()

    return handle_client

# Datos para conectarse a la red WiFi.
WLAN_SSID = "agus"
WLAN_PASSWORD = "agustinb"

# Datos para la interacción entre los terminales y el maestro.
BROADCAST_PORT = 10000
TCP_SERVER_PORT = 10001
TEAM_NAME = "Rompecircuitos"

# Variable global que indica si el terminal está conectado al maestro
master_disconnected = asyncio.Event()
master_disconnected.set()  # Inicialmente el maestro está desconectado


async def monitoring(get_app_data):
    """Monitoreo asincrónico con el controlador maestro.
    `get_app_data` es una función llamada en cada poll. Debe retornar el `dict` a enviar al maestro."""
    print(f"Controlador {TEAM_NAME}")

    if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    terminal_ip, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {terminal_ip}, Máscara de subred: {subnet_mask}")

    print("Esperando mensajes de descubrimiento y conexiones del maestro...")
    await asyncio.gather(
        listen_for_discovery_messages(
            TEAM_NAME, BROADCAST_PORT, TCP_SERVER_PORT),
        start_tcp_server(TCP_SERVER_PORT, get_app_data)
    )
